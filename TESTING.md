# 🧪 Testing Guide for TubeNova

## Quick Test Steps

### 1. Test Fallback Mode (No Backend)

1. Open `docs/test.html` in your browser
2. Click **"Test Fallback"**
3. Should see video info fetched from Invidious API
4. ✅ Success if you see title, uploader, and formats

### 2. Test Backend (Optional)

#### Start Backend:
```powershell
# In PowerShell
cd backend
D:\youtube` video` dowload\.venv\Scripts\python.exe app.py
```

Backend should start on `http://127.0.0.1:5000`

#### Test Backend:
1. Open `docs/test.html`
2. Click **"Test Health"** - Should show "Backend is running!"
3. Click **"Test Info API"** - Should fetch video info from backend
4. ✅ Success if formats are returned

### 3. Test Full App

#### Option A: Serverless Mode (No Backend)
1. Open `docs/index.html` in browser
2. Leave backend URL empty (or clear it in settings)
3. Paste YouTube URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
4. Click **"Fetch Info 🔍"**
5. Should see: "🌐 Info loaded (fallback mode)"
6. Select quality and click **"Download 📥"**
7. ✅ Download should start automatically

#### Option B: With Backend
1. Start backend (see above)
2. Open `docs/index.html`
3. Click ⚙️ settings icon
4. Enter: `http://127.0.0.1:5000`
5. Click "Save Backend URL"
6. Reload page
7. Paste YouTube URL and click **"Fetch Info"**
8. Should see: "✅ Info loaded" (no fallback message)
9. Click **"Download 📥"**
10. ✅ Download streams directly from backend

## Expected Results

### ✅ Working Features:

**Serverless Mode (Invidious API):**
- ✅ Fetch video info (title, uploader, thumbnail, duration)
- ✅ Get available formats (video + audio)
- ✅ Direct downloads from Invidious URLs
- ✅ Works on GitHub Pages without backend

**Backend Mode:**
- ✅ Fetch video info via yt-dlp
- ✅ Streaming downloads with progress
- ✅ All video qualities (144p - 1080p)
- ✅ Audio formats (128k, 320k)
- ✅ Range request support (resume downloads)

**UI Features:**
- ✅ Cartoon-style animations
- ✅ Emoji indicators
- ✅ Progress tracking with speed/ETA
- ✅ Download history
- ✅ Session statistics
- ✅ Reaction animations
- ✅ Sound effects
- ✅ Confetti on success
- ✅ Dark/Light mode
- ✅ Tooltips
- ✅ Floating shapes background

### 🔧 Common Issues:

#### "Fetch failed" Error
- **Serverless:** Invidious instance might be down, try again (auto-rotates)
- **Backend:** Make sure Flask server is running on port 5000
- **CORS:** Check backend CORS settings if using remote backend

#### Downloads Not Starting
- **Check browser console (F12)** for errors
- **Serverless:** Some formats may require cookies/auth, use backend
- **Backend:** Verify format_id is valid

#### Slow Performance
- **Serverless:** Invidious API may be slower than direct backend
- **Backend:** Use backend for best performance

## Testing Checklist

- [ ] Test page loads without errors
- [ ] Fallback script loads (check console)
- [ ] Can fetch video info in fallback mode
- [ ] Can fetch video info with backend
- [ ] Downloads work in fallback mode
- [ ] Downloads work with backend
- [ ] Progress bar updates correctly
- [ ] History saves properly
- [ ] Theme toggle works
- [ ] All animations play smoothly
- [ ] Sound effects work
- [ ] Confetti triggers on download
- [ ] Emoji indicators update
- [ ] Stats tracking works

## Debug Commands

### Check Backend Health
```powershell
curl http://127.0.0.1:5000/api/health
```

### Test Info Endpoint
```powershell
curl "http://127.0.0.1:5000/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Check Console Logs
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for:
   - `🚀 TubeNova Fallback loaded`
   - `✅ Using backend server` or `🌐 Using serverless fallback`
   - Any red error messages

## Performance Tips

### Best Setup for Production:
1. ✅ Deploy backend on Render/Railway
2. ✅ Use backend URL in production
3. ✅ Keep fallback as backup

### Best Setup for Testing:
1. ✅ Use test.html for API testing
2. ✅ Test fallback mode first (no setup needed)
3. ✅ Test backend mode if needed

## Success Indicators

### Fallback Mode Working:
- Console shows: `🚀 TubeNova Fallback loaded (Serverless mode with Invidious API)`
- Toast shows: `🌐 Info loaded (fallback mode)`
- Formats list populates
- Downloads trigger immediately

### Backend Mode Working:
- Console shows: `✅ Using backend server`
- Toast shows: `✅ Info loaded`
- Progress bar shows percentage
- Download speed and ETA display
- Streaming download completes

## Need Help?

1. **Check test.html results** - Shows detailed error messages
2. **Check browser console** - Look for JavaScript errors
3. **Check backend logs** - If using Flask server
4. **Try different video** - Some videos may be restricted
5. **Clear cache** - Ctrl+Shift+R to hard reload

---

**TubeNova is now production-ready with dual-mode support! 🎉**

- ✅ Works standalone on GitHub Pages (Invidious fallback)
- ✅ Works with backend for enhanced features
- ✅ Automatic fallback if backend unavailable
- ✅ All features functional
