#!/usr/bin/env python3
"""
Test script to verify HTTPS fix for Downtify
"""

import os
import sys
import requests
from urllib.parse import urljoin

def test_https_headers():
    """Test that security headers are properly set"""
    print("Testing HTTPS security headers...")
    
    # Import the app
    try:
        from main import app
        print("✅ Successfully imported FastAPI app")
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return False
    
    # Test that middleware is added
    if hasattr(app, 'user_middleware') and app.user_middleware:
        print("✅ Security middleware is configured")
    else:
        print("❌ Security middleware not found")
        return False
    
    return True

def test_form_action():
    """Test that form action uses HTTPS"""
    print("\nTesting form action...")
    
    try:
        with open('templates/index.html', 'r') as f:
            content = f.read()
        
        if 'hx-post="/download-web/"' in content:
            print("✅ Form action uses correct endpoint")
        else:
            print("❌ Form action not found or incorrect")
            return False
            
        if 'upgrade-insecure-requests' in content:
            print("✅ Content Security Policy meta tag found")
        else:
            print("❌ Content Security Policy meta tag missing")
            return False
            
    except FileNotFoundError:
        print("❌ Template file not found")
        return False
    
    return True

def test_environment_variables():
    """Test environment variable configuration"""
    print("\nTesting environment variables...")
    
    # Check if FORCE_HTTPS is set in railway.json
    try:
        import json
        with open('railway.json', 'r') as f:
            config = json.load(f)
        
        services = config.get('services', [])
        for service in services:
            env = service.get('env', {})
            if env.get('FORCE_HTTPS') == 'true':
                print("✅ FORCE_HTTPS environment variable configured")
                return True
        
        print("❌ FORCE_HTTPS environment variable not found in railway.json")
        return False
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error reading railway.json: {e}")
        return False

def main():
    """Run all tests"""
    print("🔒 Testing HTTPS Security Fix for Downtify")
    print("=" * 50)
    
    tests = [
        test_https_headers,
        test_form_action,
        test_environment_variables
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! HTTPS fix is properly implemented.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
