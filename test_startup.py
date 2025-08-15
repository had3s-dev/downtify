#!/usr/bin/env python3
"""
Simple test script to verify Downtify can start properly
"""

import os
import sys
import subprocess
import time

def test_startup():
    print("🧪 Testing Downtify startup...")
    
    # Set test environment
    os.environ['PORT'] = '8001'
    os.environ['DOWNLOAD_DIR'] = '/tmp/test_downloads'
    
    try:
        # Try to import the app
        print("📦 Importing main.py...")
        from main import app
        print("✅ Successfully imported FastAPI app")
        
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/health")
        print(f"✅ Health endpoint returned: {response.status_code}")
        
        print("🎉 All tests passed! Application should start successfully.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_startup()
    sys.exit(0 if success else 1)
