# 🎬 TubeNova – Download Smarter 🎧📽️

A modern, fast, and fun YouTube downloader with a **cartoon-style UI**, smooth animations, and smart serverless fallback!

**🌟 Live Demo:** [https://umeshcode1.github.io/TubeNova-YouTube-Downloader/](https://umeshcode1.github.io/TubeNova-YouTube-Downloader/)

**✨ New:** Works **without** backend! Client-side fallback mode using CORS proxies.

Live-ready structure:
- Frontend: `docs/` (GitHub Pages ready)
- Backend: `backend/` (Optional - Render/Railway/Vercel)
- Fallback: Client-side mode for serverless deployment

## 🎉 Features

### Core Features
- 📺 Paste any YouTube link (videos + Shorts)
- ⬇️ Download as Video (144p–1080p) or Audio (128k/320k)
- 🖼️ Video thumbnail, title, duration, channel info
- 🎬 Live preview (embedded YouTube player)
- 📊 Progress bar with speed/ETA tracking
- 🎊 Confetti celebration on download complete
- 🔄 No server storage: instant streaming
- 🌙 Dark/Light mode with persistence
- 📜 Download History (localStorage)
- 📈 Session analytics tracking

### Cartoon-Style UI
- 🎨 Floating shapes animation
- 🎯 Bounce & squeeze button effects
- 💫 Ripple effects on click
- 🎪 Wobble animations for icons
- ✨ Shimmer loading effects
- 💬 Cute tooltips everywhere
- 🎭 Emoji indicators & reactions
- 🎨 Hand-drawn aesthetic

### Advanced Features  
- 📋 Paste from clipboard button
- 🎵 Example video buttons
- ⚙️ Advanced options panel
- ✂️ Video trimmer controls
- 🎧 Extract audio checkbox
- 📝 Auto subtitles option
- 🖼️ Download thumbnail button
- ℹ️ Show detailed video info
- 👍❤️🔥🎉 Reaction buttons with animations
- 🎯 Floating Action Button (FAB)
- 🧹 Clear history feature
- 🎮 Tab switching (Single/Playlist/Tools)
- 🌐 Smart fallback (works without backend!)

### Developer Features
- 🔄 Auto-quality picker (based on connection)
- 🎯 Format selector (MP4/WebM/M4A/MP3)
- 🔊 Sound effects (Web Audio API)
- 🎪 Reaction overlay animations
- 📱 Fully responsive design
- ⚡ Serverless-ready with CORS proxy fallback

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript ES6+, TailwindCSS 3.x, GSAP 3.12, canvas-confetti
- **Backend:** Python Flask, yt-dlp, Flask-CORS, Requests (Optional)
- **Fallback:** CORS proxies, YouTube oEmbed API, client-side extraction
- **Deployment:** GitHub Pages + Render/Railway/Vercel (backend optional)

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
- Live URL (after build): <https://umeshcode1.github.io/TubeNova-YouTube-Downloader/>

Backend (Render)

- Create a new Web Service from this repo
- Build: `pip install -r requirements.txt` (root file includes backend requirements)
- Start: `gunicorn backend.app:app`
- Add environment: `YDL_ALLOWED_ORIGINS` (optional CSV whitelist)
- Or click: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/UmeshCode1/TubeNova-YouTube-Downloader)

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
