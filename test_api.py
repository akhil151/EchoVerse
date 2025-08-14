#!/usr/bin/env python3
"""
Test EchoVerse API endpoints
"""

import requests
import json

def test_api_endpoint():
    """Test the Flask API endpoint"""
    try:
        print("🧪 Testing Flask API endpoint...")
        
        response = requests.post(
            'http://127.0.0.1:5000/api/test-granite',
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Test Successful!")
            print(f"Status: {data.get('status')}")
            print(f"Message: {data.get('message')}")
            return True
        else:
            print(f"❌ API Test Failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API Test Exception: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        print("🏥 Testing health endpoint...")
        
        response = requests.get('http://127.0.0.1:5000/api/health', timeout=10)
        
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint exception: {e}")
        return False

def test_audiobook_creation():
    """Test audiobook creation with simple text"""
    try:
        print("🎵 Testing audiobook creation...")
        
        test_data = {
            'text': 'Hello, this is a simple test of the audiobook creation system.',
            'tone': 'professional'
        }
        
        response = requests.post(
            'http://127.0.0.1:5000/api/process',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Audiobook creation test successful!")
            print(f"Status: {data.get('status')}")
            print(f"Duration: {data.get('duration', 'Unknown')}")
            return True
        else:
            print(f"❌ Audiobook creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Audiobook creation exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 EchoVerse API Test Suite")
    print("=" * 40)
    
    # Test 1: Health
    health_ok = test_health_endpoint()
    print()
    
    # Test 2: Granite API
    granite_ok = test_api_endpoint()
    print()
    
    # Test 3: Audiobook creation (if Granite works)
    if granite_ok:
        audio_ok = test_audiobook_creation()
    else:
        audio_ok = False
        print("⏭️ Skipping audiobook test (Granite not working)")
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Granite Test: {'✅ PASS' if granite_ok else '❌ FAIL'}")
    print(f"Audiobook Creation: {'✅ PASS' if audio_ok else '❌ FAIL'}")
    
    if all([health_ok, granite_ok, audio_ok]):
        print("\n🎉 All tests passed! EchoVerse is working perfectly!")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
