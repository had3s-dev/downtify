#!/usr/bin/env python3
"""
Test script to diagnose download issues with Downtify
"""

import os
import sys
import subprocess
import requests

def test_spotdl_installation():
    """Test if spotdl is properly installed"""
    print("Testing spotdl installation...")
    
    try:
        import spotdl
        print(f"✅ spotdl version: {spotdl.__version__}")
        return True
    except ImportError as e:
        print(f"❌ spotdl not installed: {e}")
        return False

def test_yt_dlp_installation():
    """Test if yt-dlp is properly installed"""
    print("\nTesting yt-dlp installation...")
    
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ yt-dlp version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ yt-dlp error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ yt-dlp not found in PATH")
        return False

def test_ffmpeg_installation():
    """Test if ffmpeg is properly installed"""
    print("\nTesting ffmpeg installation...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg is installed")
            return True
        else:
            print(f"❌ ffmpeg error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ ffmpeg not found in PATH")
        return False

def test_spotify_credentials():
    """Test if Spotify credentials are working"""
    print("\nTesting Spotify credentials...")
    
    try:
        from main import get_spotdl
        spotdl_instance = get_spotdl()
        print("✅ Spotify credentials configured")
        return True
    except Exception as e:
        print(f"❌ Spotify credentials error: {e}")
        return False

def test_download_directory():
    """Test if download directory is accessible"""
    print("\nTesting download directory...")
    
    download_dir = os.getenv('DOWNLOAD_DIR', '/data/downloads')
    
    if os.path.exists(download_dir):
        print(f"✅ Download directory exists: {download_dir}")
        
        # Test write permissions
        try:
            test_file = os.path.join(download_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("✅ Download directory is writable")
            return True
        except Exception as e:
            print(f"❌ Download directory not writable: {e}")
            return False
    else:
        print(f"❌ Download directory does not exist: {download_dir}")
        return False

def test_network_connectivity():
    """Test network connectivity to common services"""
    print("\nTesting network connectivity...")
    
    test_urls = [
        'https://open.spotify.com',
        'https://www.youtube.com',
        'https://music.youtube.com'
    ]
    
    all_working = True
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - accessible")
            else:
                print(f"⚠️ {url} - status code: {response.status_code}")
                all_working = False
        except Exception as e:
            print(f"❌ {url} - error: {e}")
            all_working = False
    
    return all_working

def test_spotdl_search():
    """Test spotdl search functionality"""
    print("\nTesting spotdl search...")
    
    try:
        from main import get_spotdl
        spotdl_instance = get_spotdl()
        
        # Test with a simple search
        test_url = "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh"  # A popular song
        songs = spotdl_instance.search([test_url])
        
        if songs:
            print(f"✅ Search successful - found {len(songs)} song(s)")
            return True
        else:
            print("❌ Search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Diagnosing Download Issues for Downtify")
    print("=" * 60)
    
    tests = [
        test_spotdl_installation,
        test_yt_dlp_installation,
        test_ffmpeg_installation,
        test_spotify_credentials,
        test_download_directory,
        test_network_connectivity,
        test_spotdl_search
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
        print("✅ All tests passed! Download functionality should work.")
    else:
        print("❌ Some tests failed. This may explain download issues.")
        print("\n🔧 Troubleshooting suggestions:")
        print("   • Check if all dependencies are properly installed")
        print("   • Verify Spotify credentials are correct")
        print("   • Ensure download directory has write permissions")
        print("   • Check network connectivity")
        print("   • Try using Spotify URLs instead of YouTube Music URLs")
        print("   • Some YouTube Music URLs may be region-restricted")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
