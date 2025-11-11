# TubeNova – Download Smarter 🎧📽️

A modern, fast, and elegant YouTube downloader web app with a glassmorphism UI, smooth animations, and an instant streaming backend.

Live-ready structure:
- Frontend: `docs/` (GitHub Pages friendly)
- Backend: `backend/` (Render / Railway / Vercel)

## Features
- Paste any YouTube link (videos + Shorts)
- Download as Video (144p–1080p) or Audio (128/320 kbps)
- Video thumbnail, title, duration, channel
- Live preview (video/audio) before download
- Progress bar, loading spinner, toasts, confetti on success
- No storage on server: streamed instantly
- Error handling for invalid/blocked links
- Dark/Light mode with persistence
- Glassmorphism + neon glow + animated background
- Download History (localStorage) + session analytics
- Quality Auto Picker (based on connection)
- Recommended similar videos (AI-ish dummy suggestions)
- Copy Link / Share on WhatsApp
- About page + disclaimer

## Tech Stack
- Frontend: HTML, CSS, JavaScript, TailwindCSS (CDN), GSAP, canvas-confetti
- Backend: Python Flask, yt-dlp, Flask-CORS, Requests
- Deployment: GitHub Pages (frontend) + Render/Railway/Vercel (backend)

## Local Setup

1) Backend
- Install Python 3.10+
- Create venv and install requirements
- Run the Flask app

2) Frontend
- Open `docs/index.html` in a local server or browser
- Set `BACKEND_URL` in `docs/app.js` if running remotely

## Deployment

Frontend (GitHub Pages)
- Commit and push; enable Pages on main branch with `/docs` as source.

Backend (Render)
- Create a new Web Service from this repo
- Build: `pip install -r backend/requirements.txt`
- Start: `gunicorn backend.app:app`
- Add environment: `YDL_ALLOWED_ORIGINS` (optional CSV whitelist)

Backend (Railway)
- Deploy from repo, auto-detect Python; set start command: `gunicorn backend.app:app`

Backend (Vercel)
- Use a Python serverless function or Vercel Python builder; this repo includes a standard Flask server (Render/Railway recommended).

## Legal & Disclaimer
This tool is for educational and personal use only. Ensure you have rights to download the content in your jurisdiction. Respect YouTube’s Terms of Service. No copyrighted material is stored on the server; files are streamed directly.

## Credits
Developed with ❤️ by Umesh Patel

## Repo Name
TubeNova-YouTube-Downloader

---
Short summary for portfolio: Modern YouTube downloader with instant streaming backend, glassmorphism UI, animations, dark mode, history, analytics, and confetti—deployable on GitHub Pages + Render.
