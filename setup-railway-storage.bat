@echo off
echo 💾 Railway Storage Setup for Downtify
echo =====================================

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

echo 📦 Setting up Railway storage...

REM Check if we're in a Railway project
if not exist ".railway" (
    echo ❌ Not in a Railway project directory.
    echo Please run 'railway init' first or navigate to your Railway project.
    pause
    exit /b 1
)

echo 🔧 Creating storage configuration...

REM Create storage configuration
(
echo [[services]]
echo name = "downtify"
echo.
echo [[services.storage]]
echo name = "downloads"
echo path = "/data/downloads"
) > railway-storage.toml

echo ✅ Storage configuration created!
echo.
echo 📋 Next steps:
echo    1. Go to your Railway project dashboard
echo    2. Navigate to the 'Storage' tab
echo    3. Click 'Add Storage'
echo    4. Set Name: downloads
echo    5. Set Mount Path: /data/downloads
echo    6. Click 'Add Storage'
echo.
echo 🌐 Your downloads will now persist across deployments!
pause
