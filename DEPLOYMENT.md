# 🚀 TubeNova Deployment Guide

## Option 1: GitHub Pages Only (Serverless - Easiest!)

**✨ New:** TubeNova now works completely without a backend server!

### Steps:

1. **Enable GitHub Pages**
   - Go to your repository Settings
   - Navigate to "Pages" section
   - Source: Deploy from branch `main`
   - Folder: `/docs`
   - Click Save

2. **Access Your Site**
   - Your site will be live at: `https://USERNAME.github.io/REPO-NAME/`
   - Example: https://umeshcode1.github.io/TubeNova-YouTube-Downloader/

### How it Works:

- Uses **fallback.js** for client-side functionality
- Extracts video info using YouTube oEmbed API
- Uses CORS proxies to bypass restrictions
- Downloads redirect to third-party services (like ssyoutube.com)

### Limitations:

- ⚠️ Direct download not available (redirects to download services)
- ⚠️ Some advanced features require backend
- ⚠️ CORS proxies may be rate-limited

**💡 Tip:** For full functionality, deploy the backend (Option 2)

---

## Option 2: GitHub Pages + Backend (Full Features)

Deploy backend on Render, Railway, or Vercel for complete functionality.

### 2A. Deploy Backend on Render

**One-Click Deploy:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/UmeshCode1/TubeNova-YouTube-Downloader)

**Manual Steps:**

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `TubeNova-YouTube-Downloader`

3. **Configure Service**
   - **Name:** `tubenova-backend` (or your choice)
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free

4. **Environment Variables** (Optional)
   ```
   YDL_ALLOWED_ORIGINS=https://umeshcode1.github.io
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Copy your backend URL (e.g., `https://tubenova-backend.onrender.com`)

6. **Configure Frontend**
   - Visit your GitHub Pages site
   - Click the "⚙️" settings button
   - Paste your Render backend URL
   - Click "Save Backend URL"

### 2B. Deploy Backend on Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Create New Project**
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **Add Domain**
   ```bash
   railway domain
   ```

5. **Set Environment Variables**
   ```bash
   railway variables set YDL_ALLOWED_ORIGINS=https://umeshcode1.github.io
   ```

6. **Get Your URL**
   - Railway will provide a URL like: `https://tubenova-backend.railway.app`

### 2C. Deploy Backend on Vercel (Serverless)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd backend
   vercel
   ```

4. **Configure**
   - Follow prompts
   - Set root directory to `backend`
   - Vercel will auto-detect Flask

5. **Get URL**
   - Vercel provides: `https://tubenova-backend.vercel.app`

---

## Testing Your Deployment

### Test Frontend (GitHub Pages)

1. Visit your GitHub Pages URL
2. Paste a YouTube link: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
3. Click "Fetch Info 🔍"
4. Verify video info appears
5. Select quality and click "Download 📥"

### Test Backend (if deployed)

**Health Check:**
```bash
curl https://your-backend-url.com/api/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "TubeNova API is running"
}
```

**Info Endpoint:**
```bash
curl -X GET "https://your-backend-url.com/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Test Fallback Mode

1. Don't configure backend URL (leave empty)
2. Frontend should automatically use fallback mode
3. You'll see toast: "🌐 Info loaded (fallback mode)"

---

## Troubleshooting

### Frontend Not Loading

- ✅ Check GitHub Pages is enabled
- ✅ Verify `/docs` folder is set as source
- ✅ Wait 2-3 minutes for initial deployment
- ✅ Clear browser cache (Ctrl+Shift+R)

### Backend Not Working

- ✅ Check backend is deployed and running
- ✅ Verify health endpoint: `/api/health`
- ✅ Check CORS settings (YDL_ALLOWED_ORIGINS)
- ✅ View logs on Render/Railway/Vercel dashboard

### Download Fails

**Fallback Mode:**
- Click download redirects to ssyoutube.com
- This is expected behavior without backend

**Backend Mode:**
- Check backend logs for errors
- Verify format_id is valid
- Some videos may be restricted/private

### CORS Errors

**In Console:**
```
Access to fetch at '...' has been blocked by CORS policy
```

**Solution:**
- Add your GitHub Pages URL to backend environment variable:
  ```
  YDL_ALLOWED_ORIGINS=https://username.github.io
  ```

---

## Production Tips

### Performance

1. **Use Backend for Production**
   - Fallback mode is slower
   - Backend provides direct downloads
   - Better user experience

2. **Choose Nearest Region**
   - Deploy backend close to your users
   - Reduces latency

3. **Monitor Usage**
   - Watch Render/Railway logs
   - Set up alerts for errors

### Security

1. **Restrict CORS**
   - Only allow your GitHub Pages domain
   - Don't use `*` wildcard in production

2. **Rate Limiting**
   - Consider adding rate limits to backend
   - Prevent abuse

3. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade yt-dlp
   ```

### Maintenance

1. **Update yt-dlp Regularly**
   - YouTube changes their API frequently
   - Run monthly updates:
   ```bash
   pip install --upgrade yt-dlp
   git commit -am "Update yt-dlp"
   git push
   ```

2. **Monitor Issues**
   - Check GitHub Issues tab
   - Watch for user reports

3. **Backup Configuration**
   - Keep backend URL saved
   - Document custom settings

---

## Custom Domain (Optional)

### GitHub Pages Custom Domain

1. Buy domain (e.g., from Namecheap, Google Domains)
2. Add CNAME record pointing to: `username.github.io`
3. In GitHub repo Settings → Pages:
   - Enter custom domain: `tubenova.com`
   - Check "Enforce HTTPS"

### Backend Custom Domain

**Render:**
- Go to Settings → Custom Domain
- Add your domain: `api.tubenova.com`
- Update DNS CNAME to point to Render URL

**Railway:**
- Click "Settings" → "Domains"
- Add custom domain
- Update DNS records

**Vercel:**
- Go to Settings → Domains
- Add your domain
- Follow DNS configuration

---

## Need Help?

- 📖 [Check Wiki](../../wiki)
- 🐛 [Report Issues](../../issues)
- 💬 [Discussions](../../discussions)
- ⭐ [Star the Repo](../../stargazers) if you find it useful!

---

**Happy Downloading! 🎉**
