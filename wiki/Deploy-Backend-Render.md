# Deploy Backend on Render

Step-by-step guide to deploy TubeNova backend on Render (recommended hosting).

## Why Render?

- ✅ Free tier available (750 hours/month)
- ✅ Automatic HTTPS
- ✅ Easy Python deployment
- ✅ Automatic deploys from GitHub
- ✅ Built-in monitoring
- ✅ No credit card required for free tier

## Prerequisites

- GitHub account
- Render account ([Sign up free](https://render.com/))
- TubeNova repository forked/cloned

## Deployment Steps

### Method 1: One-Click Deploy (Recommended)

Click this button:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/UmeshCode1/TubeNova-YouTube-Downloader)

This will automatically configure everything!

### Method 2: Manual Setup

#### 1. Create Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub account (if not already)
4. Select **TubeNova-YouTube-Downloader** repository
5. Click **Connect**

#### 2. Configure Service

**Basic Settings:**

- **Name:** `tubenova-backend` (or your choice)
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`

**Build Settings:**

- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  gunicorn backend.app:app --preload --workers=2 --threads=2 --timeout=120
  ```

**Instance Type:**

- Select **Free** (or paid for better performance)

#### 3. Environment Variables (Optional)

Click **Advanced** → **Add Environment Variable**:

| Key                    | Value                                      |
|------------------------|--------------------------------------------|
| `YDL_ALLOWED_ORIGINS`  | `*` (or specific domains like `https://umeshcode1.github.io`) |
| `PYTHON_VERSION`       | `3.10.13` (optional, auto-detected)        |

#### 4. Deploy

1. Click **Create Web Service**
2. Wait for deployment (3-5 minutes)
3. Watch the logs for any errors

#### 5. Get Your Backend URL

Once deployed, copy your service URL:

```
https://tubenova-backend.onrender.com
```

(Replace with your actual service name)

## Configure Frontend

1. Open your deployed frontend: https://umeshcode1.github.io/TubeNova-YouTube-Downloader/
2. Click **Backend** button in header
3. Enter your Render URL: `https://tubenova-backend.onrender.com`
4. Click OK

The backend URL is saved in localStorage!

## Verify Deployment

Test health endpoint:

```bash
curl https://tubenova-backend.onrender.com/api/health
```

Expected response:

```json
{"status": "ok"}
```

Test video info:

```bash
curl "https://tubenova-backend.onrender.com/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Important Notes

### Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
  - First request after spin-down takes 30-60 seconds
  - Subsequent requests are fast
- **750 hours/month** (enough for most personal projects)
- **512 MB RAM**
- **0.1 CPU**

### Keep Service Alive (Optional)

Use a cron job or uptime monitor to ping your service:

**UptimeRobot (Free):**

1. Sign up at [UptimeRobot](https://uptimerobot.com/)
2. Add new monitor
3. URL: `https://tubenova-backend.onrender.com/api/health`
4. Interval: 5 minutes

**GitHub Actions (Free):**

```yaml
# .github/workflows/keep-alive.yml
name: Keep Alive
on:
  schedule:
    - cron: '*/14 * * * *'  # Every 14 minutes
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - run: curl https://tubenova-backend.onrender.com/api/health
```

## Automatic Deploys

Render automatically redeploys when you push to `main` branch:

```bash
git add .
git commit -m "feat: add new feature"
git push origin main
```

Render detects the push and redeploys (2-3 minutes).

## Monitoring

**View Logs:**

1. Go to Render Dashboard
2. Click your service
3. Click **Logs** tab
4. Real-time logs appear

**Check Metrics:**

- **Metrics** tab shows:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

## Custom Domain (Optional)

1. Go to **Settings** → **Custom Domains**
2. Click **Add Custom Domain**
3. Enter your domain: `api.yourdomain.com`
4. Add CNAME record in your DNS:
   ```
   CNAME api.yourdomain.com tubenova-backend.onrender.com
   ```
5. Wait for SSL certificate (5-10 minutes)

## Troubleshooting

### Deployment Failed

**Check Build Logs:**

Common issues:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Syntax errors in `backend/app.py`

**Fix:**

```bash
# Test locally first
pip install -r requirements.txt
python backend/app.py
```

### Service Crashes

**Check Runtime Logs:**

Common issues:
- Out of memory (upgrade to paid plan)
- Timeout (increase `--timeout` in start command)
- Port binding (Render sets `PORT` env var automatically)

### CORS Errors

**Set Environment Variable:**

```bash
YDL_ALLOWED_ORIGINS=https://umeshcode1.github.io
```

Or allow all origins:

```bash
YDL_ALLOWED_ORIGINS=*
```

### Slow Cold Starts

Free tier spins down. Options:

1. Use keep-alive service (see above)
2. Upgrade to paid tier (always on)
3. Accept 30-60s first request delay

## Upgrade to Paid Plan

For production apps:

- **Starter:** $7/month
  - 512 MB RAM
  - Always on (no spin-down)
  - Better performance

- **Standard:** $25/month
  - 2 GB RAM
  - Faster CPU
  - Priority support

## Next Steps

- [Deploy Frontend](Deploy-Frontend) - Host the UI
- [Custom Backend URL](Custom-Backend-URL) - Advanced configuration
- [Performance Optimization](Performance-Optimization) - Speed tips
- [API Reference](API-Reference) - Explore endpoints

## Alternative Hosting

- [Deploy on Railway](Deploy-Backend-Railway) - Alternative platform
- [Deploy on Vercel](Deploy-Backend-Vercel) - Serverless option

---

[← Back to Wiki Home](Home)
