# 🤗 Deploy TubeNova to Hugging Face Spaces

## Quick Deploy (Recommended)

### Step 1: Create Hugging Face Account
1. Go to https://huggingface.co/
2. Sign up for a free account
3. Verify your email

### Step 2: Create a New Space
1. Click on your profile → "New Space"
2. **Space name:** `tubenova-downloader`
3. **License:** MIT
4. **SDK:** Gradio
5. **Space hardware:** CPU Basic (Free)
6. Click "Create Space"

### Step 3: Upload Files
Upload these files to your Space:

**Required Files:**
- `app.py` → Upload `backend/app_hf.py` (rename to `app.py`)
- `requirements.txt` → Upload `backend/requirements_hf.txt` (rename to `requirements.txt`)

**Optional:**
- `README.md` → Upload `README_HF.md` (rename to `README.md`)

### Step 4: Wait for Build
- Hugging Face will automatically install dependencies
- Build takes ~2-3 minutes
- Your Space will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/tubenova-downloader`

---

## Alternative: Git Push Method

### Step 1: Clone Your Space
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/tubenova-downloader
cd tubenova-downloader
```

### Step 2: Copy Files
```bash
# Copy backend files
cp ../backend/app_hf.py app.py
cp ../backend/requirements_hf.txt requirements.txt
cp ../README_HF.md README.md
```

### Step 3: Commit and Push
```bash
git add .
git commit -m "Initial TubeNova deployment"
git push
```

---

## Configuration

### Environment Variables (Optional)
In your Space settings, you can add:

- `YDL_ALLOWED_ORIGINS` - CORS origins (default: `*`)
- `PORT` - Port number (default: `7860`)

### Custom Domain (Pro Feature)
Upgrade to Hugging Face Pro to get custom domains.

---

## Features

### Gradio Interface
Your Space will have a beautiful web interface with:
- ✅ YouTube URL input
- ✅ Quality selector (video/audio)
- ✅ Download button
- ✅ File output

### API Endpoints
Your Space also provides REST API:

**Base URL:** `https://YOUR_USERNAME-tubenova-downloader.hf.space`

**Endpoints:**
```bash
# Get video info
GET /api/info?url=https://youtube.com/watch?v=...

# Download video
GET /api/download?url=https://youtube.com/watch?v=...&format_id=22

# Health check
GET /api/health
```

---

## Connect Frontend to Hugging Face Backend

Update your frontend to use Hugging Face backend:

### Option 1: Manual Configuration
1. Open your live site: https://umeshcode1.github.io/TubeNova-YouTube-Downloader/
2. Click ⚙️ Settings icon
3. Enter backend URL: `https://YOUR_USERNAME-tubenova-downloader.hf.space`
4. Click "Save Backend URL"

### Option 2: Update Default Backend
Edit `docs/fallback.js`:

```javascript
// Add Hugging Face backend as default
const BACKEND = () => {
  const saved = window.BACKEND_URL || localStorage.getItem('tubenova_backend_url');
  return saved || 'https://YOUR_USERNAME-tubenova-downloader.hf.space';
};
```

---

## Advantages of Hugging Face

### ✅ Pros:
- **Free hosting** with generous limits
- **Auto-scaling** handles traffic spikes
- **Built-in Gradio UI** (bonus interface)
- **Easy deployment** (git push or web upload)
- **REST API** included automatically
- **Community visibility** on HF platform
- **GPU options** available (paid tiers)

### ⚠️ Limitations:
- **Sleep after inactivity** (free tier)
- **Resource limits** on CPU Basic
- **Build time** ~2-3 minutes on changes
- **No custom domains** (free tier)

---

## Comparison: Deployment Options

| Feature | Hugging Face | Render | Railway | Vercel |
|---------|--------------|--------|---------|---------|
| **Free Tier** | ✅ Yes | ✅ Yes | ✅ Limited | ✅ Yes |
| **Auto-scaling** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Custom Domain** | 💰 Pro | ✅ Free | ✅ Free | ✅ Free |
| **Sleep** | ✅ After 1hr | ✅ After 15min | ❌ No | ❌ No |
| **GPU Support** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Gradio UI** | ✅ Built-in | ❌ Manual | ❌ Manual | ❌ Manual |
| **Setup Time** | ⚡ 5 min | ⚡ 10 min | ⚡ 5 min | ⚡ 10 min |

**Recommendation:** Use **Hugging Face** for easy setup with bonus Gradio UI!

---

## Performance Tips

### 1. Optimize for Speed
```python
# In app_hf.py, increase chunk size for faster downloads
upstream.iter_content(chunk_size=256 * 1024)  # 256KB chunks
```

### 2. Enable Caching
Add to your Space:
```python
import functools
from functools import lru_cache

@lru_cache(maxsize=100)
def get_video_info(url):
    # Cache video info for faster repeated requests
    ...
```

### 3. Upgrade Hardware
For better performance:
- Go to Space Settings → Hardware
- Upgrade to CPU Upgrade ($0.05/hr) or T4 GPU ($0.60/hr)

---

## Monitoring

### Check Space Status
- View logs in Space → Logs tab
- See build status in Space → Build tab
- Monitor usage in Space → Metrics tab

### Health Check
```bash
curl https://YOUR_USERNAME-tubenova-downloader.hf.space/api/health
```

---

## Troubleshooting

### Space Won't Build
**Check:**
- ✅ `requirements.txt` exists
- ✅ `app.py` exists
- ✅ Python version compatibility

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python app.py
```

### API Not Responding
**Check:**
- ✅ Space is running (not sleeping)
- ✅ CORS configured correctly
- ✅ API endpoints match

**Solution:**
- Visit Space URL to wake it up
- Check Space logs for errors

### Downloads Failing
**Check:**
- ✅ yt-dlp version is latest
- ✅ Video is not age-restricted
- ✅ Video is not private

**Solution:**
```bash
# Update yt-dlp in requirements.txt
yt-dlp==2024.11.4  # Use latest version
```

---

## Advanced: Dual Backend Setup

Run both Hugging Face AND original backend:

### Primary: Hugging Face (Public)
- Use for: Public access
- URL: `https://YOUR_USERNAME-tubenova-downloader.hf.space`

### Secondary: Render/Railway (Backup)
- Use for: Fallback if HF sleeps
- URL: `https://tubenova-backend.onrender.com`

### Frontend Auto-Detection
```javascript
// In fallback.js
const BACKENDS = [
  'https://YOUR_USERNAME-tubenova-downloader.hf.space',
  'https://tubenova-backend.onrender.com',
  'http://127.0.0.1:5000'
];

async function tryBackends(url) {
  for (const backend of BACKENDS) {
    try {
      const response = await fetch(`${backend}/api/health`);
      if (response.ok) return backend;
    } catch {}
  }
  return null;
}
```

---

## Next Steps

### After Deployment:

1. ✅ **Test your Space**
   - Visit Space URL
   - Try downloading a video
   - Check API endpoints

2. ✅ **Update frontend**
   - Configure backend URL
   - Test integration
   - Verify downloads work

3. ✅ **Share your Space**
   - Add to README
   - Share on social media
   - Add to portfolio

4. ✅ **Monitor usage**
   - Check logs regularly
   - Monitor build times
   - Track errors

---

## Example Deployment

**Live Demo Spaces:**
- Official Gradio: https://huggingface.co/spaces/gradio/
- YouTube Downloader Examples: Search "youtube downloader" on HF Spaces

**Your Space will be at:**
`https://huggingface.co/spaces/YOUR_USERNAME/tubenova-downloader`

**With API at:**
`https://YOUR_USERNAME-tubenova-downloader.hf.space/api/...`

---

## Resources

- **Hugging Face Docs:** https://huggingface.co/docs/hub/spaces
- **Gradio Docs:** https://gradio.app/docs/
- **yt-dlp Docs:** https://github.com/yt-dlp/yt-dlp

---

## Support

**Issues?** Open an issue on GitHub:
https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/issues

**Questions?** Check the wiki:
https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/wiki

---

**🚀 Ready to deploy? Start with Step 1 above!**
