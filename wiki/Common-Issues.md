# Common Issues & Solutions

Troubleshooting guide for TubeNova users.

## Frontend Issues

### 1. "Backend URL not set" or Connection Failed

**Symptoms:**
- Click Fetch → No response
- Error toast appears
- Console shows network error

**Solutions:**

1. **Set Backend URL:**
   - Click **Backend** button in header
   - Enter: `http://127.0.0.1:5000` (local) or your deployed URL
   - Click OK

2. **Verify Backend is Running:**
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
   
   Should return: `{"status": "ok"}`

3. **Check CORS:**
   - Open browser DevTools (F12)
   - Check Console for CORS errors
   - See [CORS Configuration](CORS-Configuration)

---

### 2. Download Doesn't Start

**Symptoms:**
- Click Download → Nothing happens
- Progress bar doesn't move

**Solutions:**

1. **Fetch Info First:**
   - Must click **Fetch** before Download
   - Wait for thumbnail/metadata to appear

2. **Check Format Availability:**
   - Selected quality may not be available
   - Try "Auto" quality
   - Try different quality

3. **Browser Pop-up Blocker:**
   - Allow pop-ups from this site
   - Check browser notification area

---

### 3. Dark Mode Not Working

**Symptoms:**
- Toggle button doesn't change theme
- Theme doesn't persist

**Solutions:**

1. **Clear localStorage:**
   ```javascript
   // Open browser console (F12)
   localStorage.clear()
   // Reload page
   ```

2. **Check Browser Support:**
   - Update to latest browser version
   - Try different browser

---

### 4. Video Preview Not Loading

**Symptoms:**
- Thumbnail shows but preview is blank
- "Video unavailable" in preview player

**Solutions:**

1. **YouTube Embed Restrictions:**
   - Some videos can't be embedded
   - This is normal for copyright/age-restricted content
   - Download still works

2. **Ad Blocker:**
   - Temporarily disable ad blocker
   - Whitelist the site

---

## Backend Issues

### 5. "Module not found" Error

**Symptoms:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solutions:**

1. **Activate Virtual Environment:**
   ```bash
   # Windows
   .\.venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation:**
   ```bash
   pip list | grep -i flask
   ```

---

### 6. "Address already in use" (Port 5000)

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

1. **Find Process Using Port:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # macOS/Linux
   lsof -i :5000
   ```

2. **Kill Process:**
   ```bash
   # Windows (replace PID)
   taskkill /PID 12345 /F
   
   # macOS/Linux
   kill -9 12345
   ```

3. **Use Different Port:**
   Edit `backend/app.py`:
   ```python
   app.run(host='0.0.0.0', port=5001)  # Change to 5001
   ```

---

### 7. yt-dlp Extraction Failed

**Symptoms:**
```
WARNING: [youtube] Signature extraction failed
ERROR: Unable to extract video data
```

**Solutions:**

1. **Update yt-dlp:**
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Check Video Availability:**
   - Video may be private/deleted
   - Region restrictions
   - Age restrictions

3. **Test with Different Video:**
   - Try a different YouTube URL
   - Try YouTube Shorts URL

---

### 8. Download Timeout

**Symptoms:**
- Download starts but never completes
- Server shows timeout error

**Solutions:**

1. **Increase Timeout (Render/Railway):**
   
   In start command:
   ```bash
   gunicorn backend.app:app --timeout=240
   ```

2. **Check Internet Connection:**
   - Slow connection may timeout
   - Try lower quality (360p, 128k)

3. **Try Smaller File:**
   - Audio instead of video
   - Lower quality setting

---

## Deployment Issues

### 9. Render Free Tier Spins Down

**Symptoms:**
- First request takes 30-60 seconds
- "Service unavailable" initially

**Solutions:**

1. **Accept Cold Starts:**
   - Normal for free tier
   - Subsequent requests are fast

2. **Use Keep-Alive Service:**
   - [UptimeRobot](https://uptimerobot.com/) (free)
   - Pings every 5 minutes
   - Keeps service warm

3. **Upgrade to Paid Plan:**
   - $7/month Starter plan
   - Always on, no spin-down

---

### 10. GitHub Pages 404 Error

**Symptoms:**
- Navigate to Pages URL → 404
- CSS/JS not loading

**Solutions:**

1. **Check Pages Settings:**
   - Repo → Settings → Pages
   - Source: `main` branch
   - Folder: `/docs`

2. **Wait for Deployment:**
   - Takes 1-3 minutes after push
   - Check Actions tab for build status

3. **Verify File Paths:**
   - All paths in `index.html` should be relative
   - No `/docs/` prefix in URLs

---

### 11. CORS Errors in Production

**Symptoms:**
```
Access to fetch at 'https://backend.com/api/info' from origin 'https://frontend.com' 
has been blocked by CORS policy
```

**Solutions:**

1. **Set Allowed Origins:**
   
   On Render/Railway:
   ```bash
   YDL_ALLOWED_ORIGINS=https://umeshcode1.github.io
   ```

2. **Allow All Origins (Development Only):**
   ```bash
   YDL_ALLOWED_ORIGINS=*
   ```

3. **Verify Backend URL:**
   - Must be HTTPS in production
   - Check for trailing slash

See [CORS Configuration](CORS-Configuration) for details.

---

## Performance Issues

### 12. Slow Downloads

**Symptoms:**
- Download takes very long
- Progress bar moves slowly

**Solutions:**

1. **Use Auto Quality:**
   - Let the app pick best quality
   - Based on your connection

2. **Try Lower Quality:**
   - 480p instead of 1080p
   - 128k instead of 320k

3. **Check Network:**
   ```bash
   # Test backend speed
   curl -o /dev/null -w "%{speed_download}\n" http://backend.com/api/health
   ```

---

### 13. High Memory Usage

**Symptoms:**
- Backend crashes on large files
- "Out of memory" errors

**Solutions:**

1. **Increase Server Memory:**
   - Upgrade Render plan
   - Use Railway/Vercel

2. **Optimize Chunk Size:**
   
   In `backend/app.py`:
   ```python
   for chunk in upstream.iter_content(chunk_size=32*1024):  # Reduce from 64KB
   ```

3. **Use Streaming:**
   - Already implemented ✅
   - Files never stored on disk

---

## Browser-Specific Issues

### 14. Safari Download Issues

**Symptoms:**
- Downloads don't start in Safari
- Blob URL errors

**Solutions:**

1. **Update Safari:**
   - Requires Safari 14.1+

2. **Try Different Browser:**
   - Chrome, Firefox, Edge work best

3. **Use Desktop Safari:**
   - iOS Safari has limitations

---

### 15. Mobile Browser Issues

**Symptoms:**
- Layout broken on mobile
- Buttons too small
- Download doesn't work

**Solutions:**

1. **Use Latest Browser:**
   - Update Chrome/Safari on mobile

2. **Enable Desktop Mode:**
   - Temporary workaround
   - Better mobile support coming

3. **Try Desktop:**
   - Full experience on desktop

---

## Still Having Issues?

If none of these solutions work:

1. **Check Browser Console:**
   - Press F12 (DevTools)
   - Look for errors in Console tab

2. **Check Backend Logs:**
   - Render: Dashboard → Logs
   - Local: Terminal output

3. **Open GitHub Issue:**
   - [Report Bug](https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/issues/new)
   - Include:
     - Error message
     - Browser/OS version
     - Steps to reproduce

4. **Ask for Help:**
   - GitHub Discussions
   - Include console logs
   - Include backend logs

---

## Next Steps

- [FAQ](FAQ) - Frequently asked questions
- [API Reference](API-Reference) - Technical details
- [Installation Guide](Installation-Guide) - Setup from scratch

---

[← Back to Wiki Home](Home)
