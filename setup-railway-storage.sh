#!/bin/bash

# Railway Storage Setup Script for Downtify
# This script helps set up Railway storage for persistent file downloads

set -e

echo "💾 Railway Storage Setup for Downtify"
echo "====================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed."
    echo "Please install it first: npm install -g @railway/cli"
    exit 1
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway first:"
    railway login
fi

echo "📦 Setting up Railway storage..."

# Check if we're in a Railway project
if [ ! -f ".railway" ]; then
    echo "❌ Not in a Railway project directory."
    echo "Please run 'railway init' first or navigate to your Railway project."
    exit 1
fi

echo "🔧 Creating storage configuration..."

# Create storage configuration
cat > railway-storage.toml << EOF
[[services]]
name = "downtify"

[[services.storage]]
name = "downloads"
path = "/data/downloads"
EOF

echo "✅ Storage configuration created!"
echo ""
echo "📋 Next steps:"
echo "   1. Go to your Railway project dashboard"
echo "   2. Navigate to the 'Storage' tab"
echo "   3. Click 'Add Storage'"
echo "   4. Set Name: downloads"
echo "   5. Set Mount Path: /data/downloads"
echo "   6. Click 'Add Storage'"
echo ""
echo "🌐 Your downloads will now persist across deployments!"
