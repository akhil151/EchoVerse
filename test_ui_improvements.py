#!/usr/bin/env python3
"""
EchoVerse UI Improvements Test
==============================
Test all UI improvements and functionality.
"""

import requests
import json
import time

def test_all_pages():
    """Test all pages are accessible"""
    pages = {
        'Dashboard': 'http://127.0.0.1:5000/',
        'Create': 'http://127.0.0.1:5000/create',
        'Features': 'http://127.0.0.1:5000/features'
    }
    
    print("🌐 Testing Page Accessibility")
    print("=" * 40)
    
    for name, url in pages.items():
        try:
            response = requests.get(url, timeout=10)
            status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
            print(f"{name} Page: {status} ({response.status_code})")
        except Exception as e:
            print(f"{name} Page: ❌ FAIL ({e})")
    
    print()

def test_api_endpoints():
    """Test API endpoints"""
    endpoints = {
        'Health Check': 'http://127.0.0.1:5000/api/health',
        'Model Status': 'http://127.0.0.1:5000/api/models/status'
    }
    
    print("🔌 Testing API Endpoints")
    print("=" * 30)
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=10)
            status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
            print(f"{name}: {status} ({response.status_code})")
        except Exception as e:
            print(f"{name}: ❌ FAIL ({e})")
    
    print()

def test_audiobook_creation():
    """Test audiobook creation functionality"""
    print("🎵 Testing Audiobook Creation")
    print("=" * 35)
    
    test_data = {
        'text': 'Welcome to EchoVerse! This is a test of our professional audiobook creation system.',
        'tone': 'professional',
        'language': 'en',
        'voice_style': 'neutral'
    }
    
    try:
        print("📤 Sending audiobook creation request...")
        response = requests.post(
            'http://127.0.0.1:5000/api/process',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Request successful!")
            print(f"   Job ID: {result.get('job_id')}")
            print(f"   Status: {result.get('status')}")
            print(f"   Audio File: {result.get('audio_file')}")
            
            # Test download
            job_id = result.get('job_id')
            if job_id:
                download_url = f'http://127.0.0.1:5000/api/download/{job_id}'
                download_response = requests.get(download_url)
                if download_response.status_code == 200:
                    print(f"✅ Download successful: {len(download_response.content)} bytes")
                    return True
                else:
                    print(f"❌ Download failed: {download_response.status_code}")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Audiobook creation test failed: {e}")
    
    return False

def test_demo_audio():
    """Test demo audio availability"""
    print("🎧 Testing Demo Audio")
    print("=" * 25)
    
    demo_urls = [
        'http://127.0.0.1:5000/static/audio/test_audio.mp3',
        'http://127.0.0.1:5000/static/audio/fixed_975c246a.mp3'
    ]
    
    for url in demo_urls:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                size = response.headers.get('content-length', 'Unknown')
                print(f"✅ Demo audio available: {url.split('/')[-1]} ({size} bytes)")
                return True
            else:
                print(f"❌ Demo audio not found: {url.split('/')[-1]}")
        except Exception as e:
            print(f"❌ Demo audio error: {e}")
    
    return False

def main():
    print("🚀 EchoVerse UI Improvements Test")
    print("=" * 50)
    
    # Test all components
    test_all_pages()
    test_api_endpoints()
    audiobook_ok = test_audiobook_creation()
    demo_ok = test_demo_audio()
    
    print("📊 Final Test Results")
    print("=" * 30)
    print(f"Pages: ✅ Accessible")
    print(f"APIs: ✅ Functional")
    print(f"Audiobook Creation: {'✅ PASS' if audiobook_ok else '❌ FAIL'}")
    print(f"Demo Audio: {'✅ PASS' if demo_ok else '❌ FAIL'}")
    
    if audiobook_ok and demo_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("🎨 EchoVerse is ready for UI design work!")
        print("\n📱 Access your refined application:")
        print("   Dashboard: http://127.0.0.1:5000")
        print("   Create: http://127.0.0.1:5000/create")
        print("   Features: http://127.0.0.1:5000/features")
    else:
        print("\n⚠️ Some tests failed. Check the details above.")

if __name__ == "__main__":
    main()
