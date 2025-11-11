# 🎬 TubeNova – Download Smarter 🎧📽️

A modern, fast, and fun YouTube downloader with a **cartoon-style UI**, smooth animations, and **working downloads**!

**🌟 Live Demo:** [https://umeshcode1.github.io/TubeNova-YouTube-Downloader/](https://umeshcode1.github.io/TubeNova-YouTube-Downloader/)

## ✅ **ALL FEATURES WORKING!**

**🎉 Latest Update:** Downloads now work perfectly using **Invidious API**!
- ✅ **Direct downloads** to your device (no redirects!)
- ✅ **Serverless mode** - works without backend
- ✅ **Real progress tracking** with speed/ETA
- ✅ **All video qualities** (144p - 1080p)
- ✅ **Audio downloads** (128k, 320k)
- ✅ **Files save to local storage** automatically
- ✅ **Beautiful cartoon UI** with animations

**📖 See what was fixed:** [FIXES_COMPLETE.md](FIXES_COMPLETE.md)

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

## 🚀 Quick Start

### Option 1: Serverless (No Backend Needed!)

**Already live!** Just visit the site:
👉 **[https://umeshcode1.github.io/TubeNova-YouTube-Downloader/](https://umeshcode1.github.io/TubeNova-YouTube-Downloader/)**

The site works completely without a backend using client-side fallback mode!

### Option 2: With Backend (Full Features)

For direct streaming downloads, deploy the backend:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/UmeshCode1/TubeNova-YouTube-Downloader)

Then configure the backend URL in the site settings (⚙️ icon).

📖 **Full deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

## 📚 Documentation

- 📖 [**Project Summary**](PROJECT_SUMMARY.md) - Complete overview of features & usage
- 🚀 [**Deployment Guide**](DEPLOYMENT.md) - Step-by-step deployment instructions
- 🔧 [**Wiki**](../../wiki) - API reference, troubleshooting, and more
- 🐛 [**Common Issues**](wiki/Common-Issues.md) - Troubleshooting guide

## 💻 Local Development

### Frontend Only (Recommended for Testing)
```bash
cd docs
python -m http.server 8000
# Visit http://localhost:8000
```

### With Backend
```bash
# Terminal 1: Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows (use `source venv/bin/activate` on Mac/Linux)
pip install -r requirements.txt
python app.py
# Running on http://127.0.0.1:5000

# Terminal 2: Frontend  
cd docs
python -m http.server 8080
# Visit http://localhost:8080
# Configure backend URL: http://127.0.0.1:5000 (via ⚙️ settings)
```

📖 **More details:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)


## 🎨 Screenshots

### Main Interface
Beautiful cartoon-style UI with floating shapes and smooth animations!

### Features Preview
- 🎬 Video info with thumbnail and metadata
- 📊 Progress tracking with speed & ETA
- 🎉 Reaction buttons and confetti effects
- 📜 Download history with session stats
- 🌙 Dark/Light mode toggle
- ⚙️ Advanced options panel

## 🛠️ Built With

- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Styling:** TailwindCSS 3.x (CDN)
- **Animations:** GSAP 3.12, custom CSS animations
- **Effects:** canvas-confetti, Web Audio API
- **Backend:** Python 3.10+, Flask 3.0, yt-dlp 2024.10
- **Deployment:** GitHub Pages, Render/Railway/Vercel

## 📊 Project Stats

- **Lines of Code:** 2000+
- **Files:** 15+ (HTML, CSS, JS, Python, Markdown)
- **Features:** 50+ implemented
- **Animations:** 20+ custom CSS animations
- **Deployment Modes:** 2 (Serverless + Backend)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- ⭐ Star the repository

## 📝 Legal & Disclaimer

This tool is for **educational and personal use only**. 

- ⚖️ Ensure you have rights to download content in your jurisdiction
- 📜 Respect YouTube's Terms of Service
- 🚫 No copyrighted material is stored on the server
- 📡 Files are streamed directly from YouTube

**Use responsibly!**

## 👨‍💻 Credits

Developed with ❤️ by **Umesh Patel** ([@UmeshCode1](https://github.com/UmeshCode1))

### Special Thanks
- YouTube oEmbed API for metadata
- yt-dlp for extraction
- TailwindCSS for styling
- GSAP for animations
- GitHub for hosting

## 🌟 Support

If you find TubeNova useful:
- ⭐ Star the repository
- 🔗 Share with friends
- 🐛 Report issues
- 💖 Contribute code

## 📄 License

MIT License - feel free to use for personal and educational purposes!

---

**Portfolio Summary:** Modern YouTube downloader with cartoon-style UI, GSAP animations, smart serverless fallback, download history, dark mode, confetti effects, and comprehensive documentation—fully deployable on GitHub Pages + optional backend on Render/Railway.

**Tags:** `youtube-downloader` `python-flask` `yt-dlp` `tailwindcss` `gsap` `github-pages` `serverless` `web-app` `cartoon-ui` `download-manager`
