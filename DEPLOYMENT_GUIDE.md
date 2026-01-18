# AI Fitness Tracker - Global Deployment Guide

## Quick Start (5 minutes)

### Step 1: Setup Git Repository

```bash
cd /Users/karthikpalepu/Desktop/AI_Fitness_Project
git init
git add .
git commit -m "Initial commit: AI Fitness Tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-fitness-tracker.git
git push -u origin main
```

### Step 2: Deploy Backend (Choose One)

#### **Option A: Render (Easiest & Free)**

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New Web Service"
4. Select your repository
5. Configure:
   - **Name**: ai-fitness-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
   - **Root Directory**: Leave blank
6. Click "Create Web Service"
7. Wait for deployment (~2-3 min)
8. Copy the URL (e.g., `https://ai-fitness-backend-xxxxx.onrender.com`)

#### **Option B: Railway (Also Free)**

1. Go to https://railway.app
2. Create new project
3. Connect GitHub repo
4. It auto-deploys!

#### **Option C: Heroku (Paid Now)**

```bash
heroku login
heroku create ai-fitness-tracker-YOUR-NAME
git push heroku main
```

---

### Step 3: Update Frontend API Endpoint

Edit `frontend/script.js` line 1:

```javascript
const API = "https://your-backend-url.onrender.com";
```

Example:
```javascript
const API = "https://ai-fitness-backend-xyz123.onrender.com";
```

### Step 4: Deploy Frontend (Choose One)

#### **Option A: Vercel (Best for Frontend)**

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New..." → "Project"
4. Select your repository
5. Click "Deploy"
6. Your URL: `https://ai-fitness-xxxxx.vercel.app`

#### **Option B: Netlify**

1. Go to https://netlify.com
2. Create new site from Git
3. Select repository
4. Build command: (leave empty for static)
5. Publish directory: `frontend`
6. Deploy!

#### **Option C: GitHub Pages**

```bash
# Enable in GitHub settings
# Go to Settings → Pages → Source: main /root
```

---

### Step 5: Enable CORS on Backend

Add to `backend/app.py` (already done ✓):

```python
from flask_cors import CORS
CORS(app)
```

---

## Final URLs

Once deployed, share these links:

- **Frontend**: `https://ai-fitness-xxxxx.vercel.app`
- **Backend API**: `https://ai-fitness-backend-xxxxx.onrender.com`

Anyone can now access from:
- Desktop browser
- Mobile browser
- Share link with friends worldwide!

---

## Monitoring & Logs

### Render:
- Dashboard shows live logs
- Monitor in real-time

### Vercel:
- Deployment history
- Performance analytics

---

## Environment Variables (If Needed)

Create in hosting platform:

```
FLASK_ENV=production
DEBUG=False
```

---

## Troubleshooting

### 502 Bad Gateway?
- Check backend logs
- Ensure `gunicorn` is in requirements.txt

### CORS Errors?
- Verify `flask-cors` installed
- Check CORS headers in app.py

### Frontend shows blank?
- Check browser console (F12)
- Verify API endpoint is correct

---

## Cost

- **Render**: Free tier (12.5 hrs/month) or $7/month unlimited
- **Vercel**: Free forever for static sites
- **Railway**: Free tier with $5 monthly allowance
- **Netlify**: Free forever

**Total: Completely Free!** 🎉

---

## Security Tips

1. ✅ Never commit `.env` files
2. ✅ Use environment variables for sensitive data
3. ✅ Keep dependencies updated
4. ✅ Enable CORS only for your domain (optional)

---

## Next Steps

1. Create GitHub account (free)
2. Push code to repository
3. Deploy backend (5 min)
4. Deploy frontend (5 min)
5. Share with world! 🌍

**Need help? Run this command:**

```bash
./run.sh
```

This starts both servers locally for testing before deployment!

---

## Support

- **Render Support**: https://render.com/docs
- **Vercel Support**: https://vercel.com/docs
- **GitHub Help**: https://docs.github.com
