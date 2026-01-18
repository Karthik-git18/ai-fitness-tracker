#!/bin/bash

# AI Fitness Tracker - Cloud Deployment Helper

echo "🌍 AI Fitness Tracker - Global Deployment"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Initialize git repo if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: AI Fitness Tracker - Ready for deployment"
    git branch -M main
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "=========================================="
echo "📋 DEPLOYMENT STEPS:"
echo "=========================================="
echo ""
echo "1️⃣  CREATE GITHUB ACCOUNT (if needed)"
echo "   → Go to https://github.com/signup"
echo ""
echo "2️⃣  PUSH CODE TO GITHUB"
echo "   → Create new repo on GitHub (ai-fitness-tracker)"
echo "   → Then run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR-USERNAME/ai-fitness-tracker.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣  DEPLOY BACKEND (Render - 5 min)"
echo "   → Go to https://render.com"
echo "   → Sign in with GitHub"
echo "   → Click 'New Web Service'"
echo "   → Select your repository"
echo "   → Configure:"
echo "      Build: pip install -r backend/requirements.txt"
echo "      Start: gunicorn backend.app:app"
echo "   → Click 'Deploy'"
echo "   → Copy your backend URL"
echo ""
echo "4️⃣  DEPLOY FRONTEND (Vercel - 3 min)"
echo "   → Go to https://vercel.com"
echo "   → Click 'Add New Project'"
echo "   → Import your GitHub repo"
echo "   → Click 'Deploy'"
echo "   → Copy your frontend URL"
echo ""
echo "5️⃣  UPDATE API ENDPOINT"
echo "   → Edit frontend/script.js"
echo "   → Line 1: Change const API = 'http://127.0.0.1:5000'"
echo "   → To: const API = 'https://your-backend-url-on-render'"
echo ""
echo "6️⃣  PUSH UPDATE"
echo "   git add ."
echo "   git commit -m 'Update API endpoint for production'"
echo "   git push origin main"
echo ""
echo "7️⃣  VERIFY DEPLOYMENT"
echo "   → Visit your Vercel frontend URL"
echo "   → Fill in profile and test all features"
echo "   → Share link with anyone!"
echo ""
echo "=========================================="
echo "📊 EXPECTED URLS:"
echo "=========================================="
echo "Frontend: https://ai-fitness-[YOUR-PROJECT].vercel.app"
echo "Backend:  https://ai-fitness-backend-[YOUR-ID].onrender.com"
echo ""
echo "=========================================="
echo "✨ Your app is ready for the world! 🌍"
echo "=========================================="
echo ""
