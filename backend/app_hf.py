import os
import io
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import yt_dlp
import gradio as gr
from threading import Thread

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
    """Extract video information using yt-dlp"""
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
    """Download and stream video/audio"""
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
        resp.headers['Cache-Control'] = 'no-store'
        return resp
        
    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': 'DownloadError', 'detail': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'ServerError', 'detail': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'TubeNova API powered by Hugging Face'})

# Gradio Interface for Hugging Face Spaces
def gradio_download(url, quality_type, quality):
    """Gradio interface function for downloading videos"""
    try:
        # Get video info
        with yt_dlp.YoutubeDL(BASE_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
        
        title = info.get('title', 'video')
        
        # Find matching format
        format_id = None
        for f in info.get('formats', []):
            if quality_type == 'video':
                if f.get('height') and f"{f.get('height')}p" == quality:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        format_id = f['format_id']
                        break
            else:  # audio
                if f.get('abr') and f"{int(f.get('abr'))}k" == quality:
                    if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                        format_id = f['format_id']
                        break
        
        if not format_id:
            return None, f"❌ Quality {quality} not available for this video"
        
        # Download file
        output_template = f'downloads/{title[:50]}_%(format_id)s.%(ext)s'
        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'quiet': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            downloaded_file = ydl.prepare_filename(info)
        
        return downloaded_file, f"✅ Downloaded: {title}"
    
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def create_gradio_interface():
    """Create Gradio interface for Hugging Face Spaces"""
    with gr.Blocks(title="TubeNova - YouTube Downloader", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🎬 TubeNova - YouTube Downloader
        ### Powered by Hugging Face 🤗
        
        Download YouTube videos and audio in various qualities!
        """)
        
        with gr.Row():
            with gr.Column():
                url_input = gr.Textbox(
                    label="YouTube URL",
                    placeholder="https://www.youtube.com/watch?v=...",
                    lines=1
                )
                
                with gr.Row():
                    quality_type = gr.Radio(
                        choices=["video", "audio"],
                        value="video",
                        label="Type"
                    )
                
                quality_select = gr.Dropdown(
                    choices=["144p", "240p", "360p", "480p", "720p", "1080p"],
                    value="720p",
                    label="Quality",
                    interactive=True
                )
                
                download_btn = gr.Button("📥 Download", variant="primary", size="lg")
                
            with gr.Column():
                output_file = gr.File(label="Downloaded File")
                status_text = gr.Textbox(label="Status", lines=2)
        
        def update_quality_options(qtype):
            if qtype == "video":
                return gr.Dropdown(choices=["144p", "240p", "360p", "480p", "720p", "1080p"], value="720p")
            else:
                return gr.Dropdown(choices=["128k", "320k"], value="128k")
        
        quality_type.change(
            fn=update_quality_options,
            inputs=[quality_type],
            outputs=[quality_select]
        )
        
        download_btn.click(
            fn=gradio_download,
            inputs=[url_input, quality_type, quality_select],
            outputs=[output_file, status_text]
        )
        
        gr.Markdown("""
        ---
        ### Features:
        - 🎥 Download videos in multiple qualities (144p - 1080p)
        - 🎵 Download audio (128k, 320k)
        - 🚀 Fast processing with yt-dlp
        - 🤗 Hosted on Hugging Face Spaces
        
        ### API Endpoints:
        - `GET /api/info?url=<youtube_url>` - Get video information
        - `GET /api/download?url=<youtube_url>&format_id=<format>` - Download video/audio
        - `GET /api/health` - Health check
        """)
    
    return demo

# Start Flask in background thread for API access
def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 7860)), debug=False)

if __name__ == '__main__':
    # Check if running in Hugging Face Spaces
    if os.getenv('SPACE_ID'):
        print("🤗 Running on Hugging Face Spaces!")
        print("Starting Flask API in background...")
        
        # Start Flask API in background
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Launch Gradio interface
        print("Launching Gradio interface...")
        demo = create_gradio_interface()
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    else:
        # Run as standard Flask app locally
        print("🚀 Running as Flask API (local mode)")
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
