#!/usr/bin/env python3
"""
Test script to check if main.py can be imported without errors
"""

import os
import sys

def test_import():
    print("🧪 Testing main.py import...")
    
    # Set test environment
    os.environ['PORT'] = '8001'
    os.environ['DOWNLOAD_DIR'] = '/tmp/test_downloads'
    
    try:
        # Try to import main
        print("📦 Importing main.py...")
        import main
        print("✅ Successfully imported main.py")
        
        # Check if app exists
        if hasattr(main, 'app'):
            print("✅ FastAPI app found")
        else:
            print("❌ FastAPI app not found")
            return False
            
        # Check if DOWNLOAD_DIR is defined
        if hasattr(main, 'DOWNLOAD_DIR'):
            print(f"✅ DOWNLOAD_DIR: {main.DOWNLOAD_DIR}")
        else:
            print("❌ DOWNLOAD_DIR not found")
            return False
            
        print("🎉 Import test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_import()
    sys.exit(0 if success else 1)
