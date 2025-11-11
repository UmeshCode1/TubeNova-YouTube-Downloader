# Installation Guide

This guide will help you set up TubeNova locally for development or personal use.

## Prerequisites

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/UmeshCode1/TubeNova-YouTube-Downloader.git
cd TubeNova-YouTube-Downloader
```

### 2. Set Up Python Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.0.2 - Web framework
- Flask-CORS 4.0.0 - CORS support
- yt-dlp 2024.10.07 - YouTube downloader
- gunicorn 21.2.0 - Production server
- requests 2.32.3 - HTTP library

### 4. Start the Backend Server

```bash
python backend/app.py
```

You should see:

```
* Running on http://127.0.0.1:5000
```

### 5. Open the Frontend

**Option A: Direct File Access**
- Navigate to the `docs/` folder
- Open `index.html` in your web browser

**Option B: Local Server (Recommended)**

```bash
# Python 3
python -m http.server 8000 --directory docs

# Then open: http://localhost:8000
```

### 6. Configure Backend URL

1. Click the **Backend** button in the header
2. Enter: `http://127.0.0.1:5000`
3. Click OK

The URL is saved in localStorage and persists across sessions.

## Verify Installation

1. Paste a YouTube link (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Click **Fetch**
3. You should see the video thumbnail, title, and metadata
4. Select quality and click **Download**

## Troubleshooting

### "Module not found" errors

```bash
# Ensure virtual environment is activated
# Re-run: pip install -r requirements.txt
```

### Backend won't start

```bash
# Check if port 5000 is already in use
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Kill the process or change port in backend/app.py
```

### Frontend shows CORS errors

- Make sure backend is running on `http://127.0.0.1:5000`
- Check that you've set the backend URL in the UI
- Verify Flask-CORS is installed

## Next Steps

- [Quick Start Guide](Quick-Start) - Learn the features
- [Deploy Frontend](Deploy-Frontend) - Host on GitHub Pages
- [Deploy Backend](Deploy-Backend-Render) - Host on Render
- [API Reference](API-Reference) - Explore the API

## Development Setup

For contributing, also install dev dependencies:

```bash
pip install flake8 black isort
```

Run formatters:

```bash
black backend/
isort backend/
flake8 backend/
```

---

[← Back to Wiki Home](Home)
