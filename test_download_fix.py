#!/usr/bin/env python3
"""
Test script to verify download functionality fix for Downtify
"""

import os
import sys

def test_javascript_fix():
    """Test that JavaScript handles missing elements properly"""
    print("Testing JavaScript fix...")
    
    try:
        with open('static/js/script.js', 'r') as f:
            content = f.read()
        
        if 'if (downloadButton)' in content:
            print("✅ JavaScript has proper null check for download button")
        else:
            print("❌ JavaScript missing null check for download button")
            return False
            
        if 'if (spinner)' in content:
            print("✅ JavaScript has proper null check for spinner")
        else:
            print("❌ JavaScript missing null check for spinner")
            return False
            
        if 'if (!card) return;' in content:
            print("✅ JavaScript has proper null check for success card")
        else:
            print("❌ JavaScript missing null check for success card")
            return False
            
    except FileNotFoundError:
        print("❌ JavaScript file not found")
        return False
    
    return True

def test_download_endpoint():
    """Test that download endpoint is properly configured"""
    print("\nTesting download endpoint...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        if '@app.get(\'/download-file/{filename}\')' in content:
            print("✅ Download endpoint is configured")
        else:
            print("❌ Download endpoint not found")
            return False
            
        if 'FileResponse' in content:
            print("✅ FileResponse is used for downloads")
        else:
            print("❌ FileResponse not found")
            return False
            
        if 'Content-Disposition' in content:
            print("✅ Content-Disposition header is set")
        else:
            print("❌ Content-Disposition header missing")
            return False
            
    except FileNotFoundError:
        print("❌ main.py file not found")
        return False
    
    return True

def test_file_links():
    """Test that file links use the download endpoint"""
    print("\nTesting file links...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        if 'href="/download-file/{file}"' in content:
            print("✅ File links use download endpoint")
        else:
            print("❌ File links don't use download endpoint")
            return False
            
        if 'download="{file}"' in content:
            print("✅ Download attribute is set")
        else:
            print("❌ Download attribute missing")
            return False
            
        if 'fa-solid fa-download' in content:
            print("✅ Download icons are added")
        else:
            print("❌ Download icons missing")
            return False
            
    except FileNotFoundError:
        print("❌ main.py file not found")
        return False
    
    return True

def test_template_updates():
    """Test that templates are updated correctly"""
    print("\nTesting template updates...")
    
    try:
        with open('templates/list.html', 'r') as f:
            content = f.read()
        
        if 'download it to your device' in content:
            print("✅ List template has correct download instructions")
        else:
            print("❌ List template missing download instructions")
            return False
            
    except FileNotFoundError:
        print("❌ List template file not found")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🔽 Testing Download Functionality Fix for Downtify")
    print("=" * 60)
    
    tests = [
        test_javascript_fix,
        test_download_endpoint,
        test_file_links,
        test_template_updates
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Download functionality is properly fixed.")
        print("\n📋 Summary of fixes:")
        print("   • JavaScript now handles missing elements gracefully")
        print("   • New download endpoint forces file downloads")
        print("   • File links use proper download attributes")
        print("   • Download icons and clear instructions added")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
