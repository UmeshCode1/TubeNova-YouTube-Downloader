import io
import os
import json
from flask import Flask, request, jsonify, Response, make_response
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app, origins=os.getenv("YDL_ALLOWED_ORIGINS", "*").split(","))

VIDEO_QUALITIES = ["144p","240p","360p","480p","720p","1080p"]
AUDIO_BITRATES = ["128k","320k"]

# Reusable ydl opts for metadata (no download)
BASE_OPTS = {
    'quiet': True,
    'skip_download': True,
    'nocheckcertificate': True,
    'noplaylist': True,
    'extract_flat': False,
}

@app.route('/api/info')
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    try:
        with yt_dlp.YoutubeDL(BASE_OPTS) as ydl:
            data = ydl.extract_info(url, download=False)
        # Build formats list (filter only requested categories)
        formats = []
        for f in data.get('formats', []):
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                # combined av (progressive)
                height = f.get('height')
                if height and f.get('ext') in ['mp4','webm']:
                    label = f"{height}p"
                    if label in VIDEO_QUALITIES:
                        formats.append({
                            'format_id': f['format_id'],
                            'quality': label,
                            'label': label,
                            'height': height,
                            'format_note': label,
                            'filesize': f.get('filesize'),
                            'ext': f.get('ext'),
                            'type': 'video',
                            'url': f.get('url')
                        })
            elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                # audio only
                abr = f.get('abr')
                if abr:
                    label = f"{int(abr)}k"
                    if label in AUDIO_BITRATES:
                        formats.append({
                            'format_id': f['format_id'],
                            'quality': label,
                            'label': label,
                            'format_note': f"Audio {label}",
                            'abr': int(abr),
                            'filesize': f.get('filesize'),
                            'ext': f.get('ext'),
                            'acodec': f.get('acodec'),
                            'type': 'audio',
                            'url': f.get('url')
                        })
        # Deduplicate labels keeping first
        seen = set()
        cleaned = []
        for fm in formats:
            if fm['label'] not in seen:
                cleaned.append(fm)
                seen.add(fm['label'])
        resp = {
            'success': True,
            'data': {
                'id': data.get('id'),
                'title': data.get('title'),
                'uploader': data.get('uploader') or data.get('channel'),
                'duration': data.get('duration'),
                'thumbnail': data.get('thumbnail'),
                'webpage_url': data.get('webpage_url'),
                'formats': cleaned
            }
        }
        return jsonify(resp)
    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': 'DownloadError', 'detail': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'ServerError', 'detail': str(e)}), 500

@app.route('/api/download')
def download():
    url = request.args.get('url')
    format_id = request.args.get('format_id')
    if not url or not format_id:
        return jsonify({'error': 'Missing url or format_id'}), 400
    # Stream selected format
    ydl_opts = {
        'quiet': True,
        'format': format_id,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        # Find selected format
        target_format = None
        for f in info.get('formats', []):
            if f.get('format_id') == format_id:
                target_format = f
                break
        if not target_format:
            return jsonify({'error': 'FormatNotFound'}), 404

        # Guess filename + mime
        title = info.get('title') or 'tubenova'
        def sanitize(s: str) -> str:
            return ''.join(c if c.isalnum() or c in ' ._-()[]' else '_' for c in s)[:100]
        ext = target_format.get('ext') or 'bin'
        height = target_format.get('height')
        abr = target_format.get('abr')
        quality_label = (f"{height}p" if height else (f"{int(abr)}k" if abr else ''))
        filename = f"{sanitize(title)}_{quality_label}.{ext}" if quality_label else f"{sanitize(title)}.{ext}"
        # simple mime map
        mime_map = {
            'mp4': 'video/mp4', 'webm': 'video/webm', 'mkv': 'video/x-matroska',
            'm4a': 'audio/mp4', 'mp3': 'audio/mpeg', 'ogg': 'audio/ogg', 'opus': 'audio/opus',
            'wav': 'audio/wav', 'webma': 'audio/webm'
        }
        mime = mime_map.get(ext, 'application/octet-stream')

        # Proxy the bytes with Range support
        import requests
        headers = {}
        if 'Range' in request.headers:
            headers['Range'] = request.headers['Range']
        upstream = requests.get(target_format['url'], stream=True, headers=headers)

        def generate():
            for chunk in upstream.iter_content(chunk_size=64 * 1024):
                if chunk:
                    yield chunk

        status = 206 if upstream.status_code == 206 or 'Content-Range' in upstream.headers else 200
        resp = Response(generate(), status=status, mimetype=mime)
        # Pass-through length/range when available
        cl = upstream.headers.get('Content-Length')
        if cl:
            resp.headers['Content-Length'] = cl
        cr = upstream.headers.get('Content-Range')
        if cr:
            resp.headers['Content-Range'] = cr
        # Attachment filename
        resp.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        # Allow caching off to be safe
        resp.headers['Cache-Control'] = 'no-store'
        return resp
    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': 'DownloadError', 'detail': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'ServerError', 'detail': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
