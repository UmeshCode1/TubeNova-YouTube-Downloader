"""
TubeNova Backend with Hugging Face Models Integration
Enhanced with AI-powered features using pre-trained models
"""
import io
import os
import json
import re
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests
from threading import Thread
import tempfile
import base64

app = Flask(__name__)
CORS(app, origins=os.getenv("YDL_ALLOWED_ORIGINS", "*").split(","))

# Hugging Face API Configuration
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")  # Optional: for better rate limits
HF_API_BASE = "https://api-inference.huggingface.co/models"

VIDEO_QUALITIES = ["144p","240p","360p","480p","720p","1080p"]
AUDIO_BITRATES = ["128k","320k"]

# ==================== Hugging Face Model Integration ====================

def query_hf_model(model_id: str, payload: dict):
    """Query any Hugging Face Inference API model"""
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

def analyze_thumbnail(image_url: str):
    """
    Analyze video thumbnail using HF Vision models
    Model: Salesforce/blip-image-captioning-large
    """
    try:
        # Download image
        img_response = requests.get(image_url, timeout=10)
        img_data = base64.b64encode(img_response.content).decode()
        
        result = query_hf_model(
            "Salesforce/blip-image-captioning-large",
            {"inputs": img_data}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '')
        return None
    except Exception as e:
        print(f"Thumbnail analysis error: {e}")
        return None

def generate_summary(title: str, description: str):
    """
    Generate video summary using HF Language models
    Model: facebook/bart-large-cnn (summarization)
    """
    try:
        text = f"{title}. {description[:500]}" if description else title
        result = query_hf_model(
            "facebook/bart-large-cnn",
            {"inputs": text, "parameters": {"max_length": 130, "min_length": 30}}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('summary_text', '')
        return None
    except Exception as e:
        print(f"Summary generation error: {e}")
        return None

def detect_content_category(title: str, description: str):
    """
    Classify video content using zero-shot classification
    Model: facebook/bart-large-mnli
    """
    try:
        text = f"{title}. {description[:200]}" if description else title
        categories = [
            "education", "entertainment", "music", "gaming", "news",
            "sports", "technology", "tutorial", "vlog", "comedy",
            "cooking", "travel", "science", "review", "documentary"
        ]
        
        result = query_hf_model(
            "facebook/bart-large-mnli",
            {
                "inputs": text,
                "parameters": {"candidate_labels": categories}
            }
        )
        
        if isinstance(result, dict) and 'labels' in result:
            return {
                "category": result['labels'][0],
                "confidence": result['scores'][0],
                "top_3": list(zip(result['labels'][:3], result['scores'][:3]))
            }
        return None
    except Exception as e:
        print(f"Category detection error: {e}")
        return None

def analyze_sentiment(title: str, description: str):
    """
    Analyze sentiment of video content
    Model: distilbert-base-uncased-finetuned-sst-2-english
    """
    try:
        text = f"{title}. {description[:300]}" if description else title
        result = query_hf_model(
            "distilbert-base-uncased-finetuned-sst-2-english",
            {"inputs": text}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return {
                "label": result[0][0]['label'],
                "score": result[0][0]['score']
            }
        return None
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return None

def extract_keywords(text: str):
    """
    Extract keywords using NER model
    Model: dslim/bert-base-NER
    """
    try:
        result = query_hf_model(
            "dslim/bert-base-NER",
            {"inputs": text[:500]}
        )
        
        if isinstance(result, list):
            keywords = []
            for entity in result:
                if entity.get('score', 0) > 0.9:  # High confidence only
                    keywords.append({
                        "word": entity['word'],
                        "type": entity['entity_group'],
                        "score": entity['score']
                    })
            return keywords
        return None
    except Exception as e:
        print(f"Keyword extraction error: {e}")
        return None

def detect_language(text: str):
    """
    Detect language of video content
    Model: papluca/xlm-roberta-base-language-detection
    """
    try:
        result = query_hf_model(
            "papluca/xlm-roberta-base-language-detection",
            {"inputs": text[:200]}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return {
                "language": result[0][0]['label'],
                "confidence": result[0][0]['score']
            }
        return None
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

def suggest_title_improvement(title: str):
    """
    Suggest improved title using text generation
    Model: google/flan-t5-base
    """
    try:
        prompt = f"Improve this YouTube video title for better engagement: {title}"
        result = query_hf_model(
            "google/flan-t5-base",
            {"inputs": prompt, "parameters": {"max_length": 100}}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '')
        return None
    except Exception as e:
        print(f"Title improvement error: {e}")
        return None

# ==================== Enhanced API Endpoints ====================

BASE_OPTS = {
    'quiet': True,
    'skip_download': True,
    'nocheckcertificate': True,
    'noplaylist': True,
    'extract_flat': False,
}

@app.route('/api/info')
def info():
    """Enhanced video info with AI analysis"""
    url = request.args.get('url')
    ai_analysis = request.args.get('ai', 'false').lower() == 'true'
    
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    
    try:
        with yt_dlp.YoutubeDL(BASE_OPTS) as ydl:
            data = ydl.extract_info(url, download=False)
        
        # Build formats list
        formats = []
        for f in data.get('formats', []):
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
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
        
        # Deduplicate
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
            'formats': cleaned
        }
        
        # Add AI-powered analysis if requested
        if ai_analysis:
            title = data.get('title', '')
            description = data.get('description', '')
            thumbnail = data.get('thumbnail', '')
            
            ai_features = {}
            
            # Run AI analysis in parallel (non-blocking for better performance)
            if thumbnail:
                ai_features['thumbnail_analysis'] = analyze_thumbnail(thumbnail)
            
            if description:
                ai_features['summary'] = generate_summary(title, description)
                ai_features['category'] = detect_content_category(title, description)
                ai_features['sentiment'] = analyze_sentiment(title, description)
                ai_features['keywords'] = extract_keywords(f"{title}. {description}")
                ai_features['language'] = detect_language(f"{title}. {description}")
            
            if title:
                ai_features['suggested_title'] = suggest_title_improvement(title)
            
            response_data['ai_analysis'] = ai_features
        
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
    """Stream download with original functionality"""
    url = request.args.get('url')
    format_id = request.args.get('format_id')
    if not url or not format_id:
        return jsonify({'error': 'Missing url or format_id'}), 400
    
    ydl_opts = {
        'quiet': True,
        'format': format_id,
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        target_format = None
        for f in info.get('formats', []):
            if f.get('format_id') == format_id:
                target_format = f
                break
        
        if not target_format:
            return jsonify({'error': 'FormatNotFound'}), 404

        title = info.get('title') or 'tubenova'
        def sanitize(s: str) -> str:
            return ''.join(c if c.isalnum() or c in ' ._-()[]' else '_' for c in s)[:100]
        
        ext = target_format.get('ext') or 'bin'
        height = target_format.get('height')
        abr = target_format.get('abr')
        quality_label = (f"{height}p" if height else (f"{int(abr)}k" if abr else ''))
        filename = f"{sanitize(title)}_{quality_label}.{ext}" if quality_label else f"{sanitize(title)}.{ext}"
        
        mime_map = {
            'mp4': 'video/mp4', 'webm': 'video/webm', 'mkv': 'video/x-matroska',
            'm4a': 'audio/mp4', 'mp3': 'audio/mpeg', 'ogg': 'audio/ogg', 'opus': 'audio/opus',
            'wav': 'audio/wav', 'webma': 'audio/webm'
        }
        mime = mime_map.get(ext, 'application/octet-stream')

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
        
        cl = upstream.headers.get('Content-Length')
        if cl:
            resp.headers['Content-Length'] = cl
        cr = upstream.headers.get('Content-Range')
        if cr:
            resp.headers['Content-Range'] = cr
        
        resp.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
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
    Analyze video without downloading
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
        
        analysis = {
            'video_info': {
                'title': title,
                'uploader': data.get('uploader'),
                'duration': data.get('duration'),
                'view_count': data.get('view_count'),
                'like_count': data.get('like_count'),
            },
            'ai_insights': {}
        }
        
        # Run all AI models
        if thumbnail:
            analysis['ai_insights']['thumbnail_caption'] = analyze_thumbnail(thumbnail)
        
        if description:
            analysis['ai_insights']['summary'] = generate_summary(title, description)
            analysis['ai_insights']['category'] = detect_content_category(title, description)
            analysis['ai_insights']['sentiment'] = analyze_sentiment(title, description)
            analysis['ai_insights']['keywords'] = extract_keywords(f"{title}. {description}")
            analysis['ai_insights']['language'] = detect_language(f"{title}. {description}")
        
        if title:
            analysis['ai_insights']['improved_title'] = suggest_title_improvement(title)
        
        return jsonify({'success': True, 'data': analysis})
        
    except Exception as e:
        return jsonify({'error': 'AnalysisError', 'detail': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'TubeNova API with Hugging Face AI Models',
        'features': [
            'Image Captioning (BLIP)',
            'Text Summarization (BART)',
            'Zero-Shot Classification',
            'Sentiment Analysis',
            'Named Entity Recognition',
            'Language Detection',
            'Title Improvement (FLAN-T5)'
        ]
    })

@app.route('/api/models')
def models_info():
    """Information about integrated HF models"""
    return jsonify({
        'models': [
            {
                'name': 'BLIP Image Captioning',
                'id': 'Salesforce/blip-image-captioning-large',
                'task': 'Image-to-Text',
                'description': 'Analyzes video thumbnails and generates captions'
            },
            {
                'name': 'BART Summarization',
                'id': 'facebook/bart-large-cnn',
                'task': 'Summarization',
                'description': 'Generates concise summaries of video content'
            },
            {
                'name': 'BART Zero-Shot Classification',
                'id': 'facebook/bart-large-mnli',
                'task': 'Zero-Shot Classification',
                'description': 'Categorizes video content into 15+ categories'
            },
            {
                'name': 'DistilBERT Sentiment',
                'id': 'distilbert-base-uncased-finetuned-sst-2-english',
                'task': 'Sentiment Analysis',
                'description': 'Analyzes positive/negative sentiment'
            },
            {
                'name': 'BERT NER',
                'id': 'dslim/bert-base-NER',
                'task': 'Named Entity Recognition',
                'description': 'Extracts people, places, organizations from text'
            },
            {
                'name': 'XLM-RoBERTa Language Detection',
                'id': 'papluca/xlm-roberta-base-language-detection',
                'task': 'Language Identification',
                'description': 'Detects the language of video content'
            },
            {
                'name': 'FLAN-T5 Text Generation',
                'id': 'google/flan-t5-base',
                'task': 'Text Generation',
                'description': 'Suggests improved video titles'
            }
        ],
        'usage': {
            'basic': 'Add ?ai=true to /api/info endpoint',
            'dedicated': 'Use /api/analyze endpoint for full AI analysis',
            'api_token': 'Set HF_API_TOKEN env var for higher rate limits'
        }
    })

# ==================== Gradio Integration (for HF Spaces) ====================

try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

if GRADIO_AVAILABLE and os.getenv('SPACE_ID'):
    def gradio_download(url, quality_type, quality, enable_ai):
        """Gradio interface download function with AI analysis"""
        try:
            # Get video info with AI analysis
            with yt_dlp.YoutubeDL(BASE_OPTS) as ydl:
                info = ydl.extract_info(url, download=False)
            
            # AI Analysis
            ai_text = "AI Analysis: Disabled"
            if enable_ai:
                title = info.get('title', '')
                description = info.get('description', '')
                
                ai_results = []
                
                # Category
                category = detect_content_category(title, description)
                if category:
                    ai_results.append(f"📂 Category: {category['category']} ({category['confidence']:.2%})")
                
                # Sentiment
                sentiment = analyze_sentiment(title, description)
                if sentiment:
                    ai_results.append(f"😊 Sentiment: {sentiment['label']} ({sentiment['score']:.2%})")
                
                # Language
                language = detect_language(f"{title}. {description}")
                if language:
                    ai_results.append(f"🌍 Language: {language['language']} ({language['confidence']:.2%})")
                
                # Summary
                summary = generate_summary(title, description)
                if summary:
                    ai_results.append(f"📝 Summary: {summary}")
                
                ai_text = "\n".join(ai_results) if ai_results else "AI Analysis: No results"
            
            # Find format
            format_id = None
            if quality_type == "Video":
                for f in info.get('formats', []):
                    if f.get('height') and f"{f['height']}p" == quality:
                        format_id = f['format_id']
                        break
            else:  # Audio
                for f in info.get('formats', []):
                    if f.get('abr') and f"{int(f['abr'])}k" == quality:
                        format_id = f['format_id']
                        break
            
            if not format_id:
                return None, f"❌ Format not found\n\n{ai_text}"
            
            # Download
            ydl_opts = {
                'format': format_id,
                'outtmpl': tempfile.gettempdir() + '/%(title)s_%(resolution)s.%(ext)s',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(result)
            
            return filename, f"✅ Downloaded successfully!\n\n{ai_text}"
            
        except Exception as e:
            return None, f"❌ Error: {str(e)}"
    
    def create_gradio_interface():
        """Create Gradio interface with AI features"""
        with gr.Blocks(theme=gr.themes.Soft(), title="TubeNova AI Downloader") as demo:
            gr.Markdown("# 🎬 TubeNova AI - YouTube Downloader with Hugging Face Models")
            gr.Markdown("Powered by 7+ pre-trained AI models for intelligent video analysis!")
            
            with gr.Row():
                with gr.Column():
                    url_input = gr.Textbox(
                        label="YouTube URL",
                        placeholder="https://youtube.com/watch?v=...",
                        lines=1
                    )
                    
                    with gr.Row():
                        quality_type = gr.Radio(
                            choices=["Video", "Audio"],
                            value="Video",
                            label="Type"
                        )
                        quality = gr.Dropdown(
                            choices=VIDEO_QUALITIES,
                            value="720p",
                            label="Quality"
                        )
                    
                    enable_ai = gr.Checkbox(
                        label="🤖 Enable AI Analysis (Category, Sentiment, Summary, etc.)",
                        value=True
                    )
                    
                    download_btn = gr.Button("⬇️ Download", variant="primary", size="lg")
                
                with gr.Column():
                    output_file = gr.File(label="Downloaded File")
                    output_text = gr.Textbox(label="Status & AI Analysis", lines=10)
            
            # Update quality dropdown based on type
            def update_quality(qtype):
                if qtype == "Video":
                    return gr.Dropdown(choices=VIDEO_QUALITIES, value="720p")
                else:
                    return gr.Dropdown(choices=AUDIO_BITRATES, value="128k")
            
            quality_type.change(fn=update_quality, inputs=quality_type, outputs=quality)
            
            download_btn.click(
                fn=gradio_download,
                inputs=[url_input, quality_type, quality, enable_ai],
                outputs=[output_file, output_text]
            )
            
            gr.Markdown("""
            ### 🤗 AI Models Used:
            - **BLIP**: Image captioning for thumbnails
            - **BART**: Text summarization & classification
            - **DistilBERT**: Sentiment analysis
            - **BERT**: Named entity recognition
            - **XLM-RoBERTa**: Language detection
            - **FLAN-T5**: Title improvement suggestions
            
            ### 📡 API Endpoints:
            - `GET /api/info?url=<URL>&ai=true` - Video info with AI analysis
            - `GET /api/download?url=<URL>&format_id=<ID>` - Download video
            - `GET /api/analyze?url=<URL>` - Dedicated AI analysis
            - `GET /api/models` - List all HF models
            - `GET /api/health` - Health check
            """)
        
        return demo
    
    # Run Flask + Gradio
    def run_flask():
        app.run(host='0.0.0.0', port=7860, debug=False)
    
    print("🤗 Running on Hugging Face Spaces with AI Models!")
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)

elif __name__ == '__main__':
    print("🏠 Running locally - Flask only mode")
    print("💡 Set SPACE_ID env var and install gradio for Gradio UI")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
