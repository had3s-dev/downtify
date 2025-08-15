@echo off
echo 🚂 Railway Deployment Script for Downtify
echo ==========================================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Railway CLI is not installed.
    echo Please install it first: npm install -g @railway/cli
    pause
    exit /b 1
)

REM Check if user is logged in
railway whoami >nul 2>&1
if errorlevel 1 (
    echo 🔐 Please login to Railway first:
    railway login
)

echo 📦 Initializing Railway project...
railway init

echo 🔧 Setting up environment variables...
railway variables set DOWNLOAD_DIR=/tmp/downloads

echo 🚀 Deploying to Railway...
railway up

echo ✅ Deployment complete!
echo.
echo 🌐 Your app is now deployed!
echo 📋 Next steps:
echo    1. Go to your Railway dashboard
echo    2. Add your custom domain: music.nexusremains.online
echo    3. Configure DNS records as provided by Railway
echo    4. Set up Spotify credentials if needed
echo.
echo 📖 For detailed instructions, see: RAILWAY_DEPLOYMENT.md
pause
