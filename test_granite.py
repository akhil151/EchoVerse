#!/usr/bin/env python3
"""
Quick Granite Model Test Script
Run this to quickly test if IBM Granite 3.2 is working
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_granite_direct():
    """Test Granite model directly"""
    granite_url = os.getenv('GRANITE_API_URL')
    
    if not granite_url:
        print("❌ No GRANITE_API_URL found in .env file!")
        return False
    
    print(f"🧪 Testing IBM Granite 3.2 at: {granite_url}")
    
    try:
        # Test the health endpoint first
        health_url = f"{granite_url}/health"
        print(f"📡 Testing health endpoint: {health_url}")
        
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
        else:
            print(f"⚠️ Health check returned status: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    try:
        # Test text transformation
        test_data = {
            "text": "Hello, this is a test message.",
            "tone": "professional"
        }

        transform_url = f"{granite_url}/transform"
        print(f"🔄 Testing text transformation: {transform_url}")
        
        response = requests.post(
            transform_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Text transformation successful!")
            print(f"📝 Original: {test_data['text']}")
            print(f"✨ Transformed: {result.get('transformed_text', 'No transformed text returned')}")
            return True
        else:
            print(f"❌ Transformation failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Text enhancement failed: {e}")
        return False

def test_flask_granite():
    """Test Granite through Flask API"""
    print("\n🌐 Testing through Flask API...")
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/test-granite',
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Flask API test: {result['status']}")
            print(f"📝 Message: {result['message']}")
            return True
        else:
            print(f"❌ Flask API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Flask API test failed: {e}")
        return False

def main():
    print("🚀 EchoVerse Granite Model Test")
    print("=" * 50)
    
    # Test 1: Direct Granite connection
    print("\n1️⃣ Testing Direct Granite Connection")
    direct_success = test_granite_direct()
    
    # Test 2: Flask API connection
    print("\n2️⃣ Testing Flask API Connection")
    flask_success = test_flask_granite()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    print(f"Direct Granite: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"Flask API: {'✅ PASS' if flask_success else '❌ FAIL'}")
    
    if direct_success and flask_success:
        print("\n🎉 All tests passed! Audio generation should work.")
        print("💡 Try creating an audiobook now!")
    elif direct_success and not flask_success:
        print("\n⚠️ Granite works but Flask has issues. Restart Flask app.")
    elif not direct_success:
        print("\n❌ Granite model not accessible. Check Colab and URL.")
        print("\n🔧 Next Steps:")
        print("1. Restart Google Colab")
        print("2. Copy new ngrok URL")
        print("3. Run: python update_colab_url.py")
        print("4. Restart Flask: python app.py")
    
    print(f"\n🔗 Current Granite URL: {os.getenv('GRANITE_API_URL', 'Not set')}")

if __name__ == "__main__":
    main()
