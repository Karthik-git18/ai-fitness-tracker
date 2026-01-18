# 🚀 Deployment Guide - AI Fitness Tracker

## Option 1: Deploy Backend on Render (Recommended - Free)

### Backend Setup:
1. Go to https://render.com and create account
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Fill in:
   - **Name**: ai-fitness-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click "Create Web Service"

Your backend URL will be: `https://ai-fitness-backend-xxxxx.onrender.com`

---

## Option 2: Deploy Frontend on Vercel (Recommended - Free)

### Frontend Setup:
1. Go to https://vercel.com and create account
2. Click "Add New..." → "Project"
3. Import GitHub repo
4. Click "Deploy"

Your frontend URL will be: `https://ai-fitness-xxxxx.vercel.app`

---

## Option 3: Deploy on Railway (Simple - Free tier)

### Both Backend & Frontend:
1. Go to https://railway.app
2. Create project
3. Add GitHub repo
4. It auto-detects Flask and deploys

---

## Option 4: Deploy on Heroku (Free tier ending - Paid)

If you have Heroku account:
```bash
heroku create ai-fitness-tracker
git push heroku main
```

---

## Step-by-Step Quick Setup

### 1️⃣ Update Frontend API Endpoint

Edit `frontend/script.js` - Change line 1:
```javascript
const API = "YOUR_DEPLOYED_BACKEND_URL";
// Example: const API = "https://ai-fitness-backend-xxxxx.onrender.com";
```

### 2️⃣ Add CORS Headers (Already done ✓)

Your backend has `CORS` enabled, so cross-origin requests work.

### 3️⃣ Create Production Files

Backend needs `Procfile` and updated `requirements.txt`.

---

## What You Need to Do Now

1. **Choose a hosting service** (Render recommended)
2. **Push code to GitHub**
3. **Deploy backend** → Get URL
4. **Update API endpoint** in script.js
5. **Deploy frontend** → Get public URL
6. **Share URL** with anyone worldwide!

---

## Manual Deployment (Advanced)

If you want to use your own server (AWS, DigitalOcean, etc.):

```bash
# Install dependencies
pip install -r requirements.txt
npm install -g http-server

# Start production servers
gunicorn app:app --bind 0.0.0.0:5000
http-server frontend --port 8080 --cors
```

---

## Environment Variables

Create `.env` file in backend:
```
FLASK_ENV=production
DEBUG=False
```

---

## Testing Deployment

After deployment:
1. Visit frontend URL
2. Fill in profile
3. Check all features work
4. Share URL with friends!

---

**Need help? Ask me to:**
- Set up GitHub repo
- Create Procfile
- Configure Render deployment
- Update API endpoints
