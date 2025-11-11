import io
import os
import json
import base64
from flask import Flask, request, jsonify, Response, make_response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app, origins=os.getenv("YDL_ALLOWED_ORIGINS", "*").split(","))

VIDEO_QUALITIES = ["144p","240p","360p","480p","720p","1080p"]
AUDIO_BITRATES = ["128k","320k"]

# Hugging Face API Configuration
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")  # Optional: set for higher rate limits
HF_API_BASE = "https://api-inference.huggingface.co/models"

# Reusable ydl opts for metadata (no download)
BASE_OPTS = {
    'quiet': True,
    'skip_download': True,
    'nocheckcertificate': True,
    'noplaylist': True,
    'extract_flat': False,
}

# ==================== Hugging Face Models Integration ====================

def query_hf_model(model_id: str, payload: dict):
    """Query Hugging Face Inference API"""
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}
    try:
        response = requests.post(
            f"{HF_API_BASE}/{model_id}",
            headers=headers,
            json=payload,
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def analyze_with_ai(title: str, description: str, thumbnail: str = None):
    """AI-powered video analysis using multiple HF models"""
    ai_results = {}
    
    try:
        # 1. Category Detection (Zero-Shot Classification)
        text = f"{title}. {description[:200]}" if description else title
        categories = ["education", "entertainment", "music", "gaming", "news",
                     "sports", "technology", "tutorial", "vlog", "comedy"]
        
        category_result = query_hf_model(
            "facebook/bart-large-mnli",
            {"inputs": text, "parameters": {"candidate_labels": categories}}
        )
        
        if isinstance(category_result, dict) and 'labels' in category_result:
            ai_results['category'] = {
                "primary": category_result['labels'][0],
                "confidence": round(category_result['scores'][0] * 100, 2),
                "alternatives": list(zip(category_result['labels'][1:3], 
                                       [round(s*100, 2) for s in category_result['scores'][1:3]]))
            }
        
        # 2. Sentiment Analysis
        sentiment_result = query_hf_model(
            "distilbert-base-uncased-finetuned-sst-2-english",
            {"inputs": text[:512]}
        )
        
        if isinstance(sentiment_result, list) and len(sentiment_result) > 0:
            ai_results['sentiment'] = {
                "label": sentiment_result[0][0]['label'],
                "score": round(sentiment_result[0][0]['score'] * 100, 2)
            }
        
        # 3. Language Detection
        lang_result = query_hf_model(
            "papluca/xlm-roberta-base-language-detection",
            {"inputs": text[:200]}
        )
        
        if isinstance(lang_result, list) and len(lang_result) > 0:
            ai_results['language'] = {
                "code": lang_result[0][0]['label'],
                "confidence": round(lang_result[0][0]['score'] * 100, 2)
            }
        
        # 4. Content Summary (if description available)
        if description and len(description) > 50:
            summary_result = query_hf_model(
                "facebook/bart-large-cnn",
                {"inputs": f"{title}. {description[:1000]}", 
                 "parameters": {"max_length": 100, "min_length": 30}}
            )
            
            if isinstance(summary_result, list) and len(summary_result) > 0:
                ai_results['summary'] = summary_result[0].get('summary_text', '')
        
        # 5. Thumbnail Analysis (if available)
        if thumbnail:
            try:
                img_response = requests.get(thumbnail, timeout=10)
                if img_response.status_code == 200:
                    img_data = base64.b64encode(img_response.content).decode()
                    
                    caption_result = query_hf_model(
                        "Salesforce/blip-image-captioning-large",
                        {"inputs": img_data}
                    )
                    
                    if isinstance(caption_result, list) and len(caption_result) > 0:
                        ai_results['thumbnail_caption'] = caption_result[0].get('generated_text', '')
            except:
                pass  # Thumbnail analysis is optional
        
    except Exception as e:
        ai_results['error'] = str(e)
    
    return ai_results

@app.route('/api/info')
def info():
    url = request.args.get('url')
    ai_enabled = request.args.get('ai', 'false').lower() == 'true'
    
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
        
        response_data = {
            'id': data.get('id'),
            'title': data.get('title'),
            'uploader': data.get('uploader') or data.get('channel'),
            'duration': data.get('duration'),
            'thumbnail': data.get('thumbnail'),
            'webpage_url': data.get('webpage_url'),
            'description': data.get('description', '')[:500],
            'view_count': data.get('view_count'),
            'like_count': data.get('like_count'),
            'formats': cleaned
        }
        
        # Add AI analysis if requested
        if ai_enabled:
            title = data.get('title', '')
            description = data.get('description', '')
            thumbnail = data.get('thumbnail', '')
            
            ai_analysis = analyze_with_ai(title, description, thumbnail)
            response_data['ai_analysis'] = ai_analysis
        
        resp = {
            'success': True,
            'data': response_data
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

@app.route('/api/analyze')
def analyze():
    """
    Dedicated AI analysis endpoint
    Returns comprehensive AI insights without downloading
    """
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    
    try:
        with yt_dlp.YoutubeDL(BASE_OPTS) as ydl:
            data = ydl.extract_info(url, download=False)
        
        title = data.get('title', '')
        description = data.get('description', '')
        thumbnail = data.get('thumbnail', '')
        
        # Get comprehensive AI analysis
        ai_insights = analyze_with_ai(title, description, thumbnail)
        
        result = {
            'success': True,
            'data': {
                'video_info': {
                    'title': title,
                    'uploader': data.get('uploader'),
                    'duration': data.get('duration'),
                    'view_count': data.get('view_count'),
                    'like_count': data.get('like_count'),
                },
                'ai_insights': ai_insights
            }
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'AnalysisError', 'detail': str(e)}), 500

@app.route('/api/models')
def models_info():
    """List all integrated Hugging Face models"""
    return jsonify({
        'success': True,
        'models': [
            {
                'name': 'BART Zero-Shot Classification',
                'id': 'facebook/bart-large-mnli',
                'task': 'Zero-Shot Classification',
                'description': 'Categorizes videos into 10+ categories',
                'categories': ['education', 'entertainment', 'music', 'gaming', 'news',
                              'sports', 'technology', 'tutorial', 'vlog', 'comedy']
            },
            {
                'name': 'DistilBERT Sentiment Analysis',
                'id': 'distilbert-base-uncased-finetuned-sst-2-english',
                'task': 'Sentiment Analysis',
                'description': 'Analyzes positive/negative sentiment of video content'
            },
            {
                'name': 'XLM-RoBERTa Language Detection',
                'id': 'papluca/xlm-roberta-base-language-detection',
                'task': 'Language Identification',
                'description': 'Detects the language of video content'
            },
            {
                'name': 'BART CNN Summarization',
                'id': 'facebook/bart-large-cnn',
                'task': 'Text Summarization',
                'description': 'Generates concise summaries of video descriptions'
            },
            {
                'name': 'BLIP Image Captioning',
                'id': 'Salesforce/blip-image-captioning-large',
                'task': 'Image-to-Text',
                'description': 'Analyzes video thumbnails and generates captions'
            }
        ],
        'usage': {
            'basic_info': 'GET /api/info?url=<URL>&ai=true',
            'dedicated_analysis': 'GET /api/analyze?url=<URL>',
            'api_token': 'Set HF_API_TOKEN environment variable for higher rate limits',
            'rate_limits': 'Free tier: ~1000 requests/day per model'
        }
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'TubeNova API powered by Hugging Face AI Models',
        'version': '2.0',
        'features': {
            'basic': ['Video download', 'Audio extraction', 'Format selection'],
            'ai_powered': ['Content categorization', 'Sentiment analysis', 'Language detection', 
                          'Summary generation', 'Thumbnail analysis']
        },
        'endpoints': ['/api/info', '/api/download', '/api/analyze', '/api/models', '/api/health']
    })

if __name__ == '__main__':
    print("🤗 TubeNova Backend with Hugging Face AI Models")
    print("📡 Available endpoints:")
    print("   - GET /api/info?url=<URL>&ai=true (with AI analysis)")
    print("   - GET /api/download?url=<URL>&format_id=<ID>")
    print("   - GET /api/analyze?url=<URL> (dedicated AI analysis)")
    print("   - GET /api/models (list HF models)")
    print("   - GET /api/health (status check)")
    print("\n💡 Tip: Set HF_API_TOKEN environment variable for better rate limits!")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
