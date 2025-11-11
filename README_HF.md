---
title: TubeNova YouTube Downloader
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.44.0
app_file: backend/app_hf.py
pinned: false
license: mit
---

# 🎬 TubeNova - YouTube Downloader

A modern, beautiful YouTube downloader with a cartoon-style UI and powerful backend!

## Features

- 🎥 Download videos in multiple qualities (144p - 1080p)
- 🎵 Download audio (128k, 320k)
- 🚀 Fast processing with yt-dlp
- 🤗 Hosted on Hugging Face Spaces
- 🎨 Beautiful Gradio interface
- 🔌 RESTful API available

## Usage

### Web Interface
Simply paste a YouTube URL, select quality, and click download!

### API Endpoints

**Get Video Info:**
```bash
GET /api/info?url=<youtube_url>
```

**Download Video/Audio:**
```bash
GET /api/download?url=<youtube_url>&format_id=<format_id>
```

**Health Check:**
```bash
GET /api/health
```

## Local Development

```bash
pip install -r backend/requirements_hf.txt
python backend/app_hf.py
```

## Technologies

- **Backend:** Python Flask + yt-dlp
- **Interface:** Gradio
- **Hosting:** Hugging Face Spaces
- **API:** RESTful endpoints

## Links

- **GitHub:** https://github.com/UmeshCode1/TubeNova-YouTube-Downloader
- **Live Site:** https://umeshcode1.github.io/TubeNova-YouTube-Downloader/

## License

MIT License - See LICENSE file for details
