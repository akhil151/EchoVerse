#!/usr/bin/env python3
"""
Debug Dashboard Error
"""

import requests
import traceback

def test_dashboard():
    try:
        print("🔍 Testing dashboard...")
        response = requests.get('http://127.0.0.1:5000/', timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Error Response:")
            print(response.text[:1000])  # First 1000 chars
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard()
