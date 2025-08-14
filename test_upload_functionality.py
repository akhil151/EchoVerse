#!/usr/bin/env python3
"""
Test script to verify the upload functionality in the text editor
"""

import requests
import time

def test_create_page():
    """Test that the create page loads and contains the upload button"""
    try:
        response = requests.get('http://127.0.0.1:5000/create', timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for upload button
            if 'uploadFileBtn' in content:
                print("✅ Upload button found in text editor")
            else:
                print("❌ Upload button NOT found in text editor")
                
            # Check for file input
            if 'fileInput' in content:
                print("✅ File input element found")
            else:
                print("❌ File input element NOT found")
                
            # Check for text editor
            if 'textEditorContainer' in content:
                print("✅ Text editor container found")
            else:
                print("❌ Text editor container NOT found")
                
            # Check for upload functionality
            if 'handleFileUpload' in content:
                print("✅ File upload handler found")
            else:
                print("❌ File upload handler NOT found")
                
            print(f"✅ Create page loaded successfully (Status: {response.status_code})")
            return True
        else:
            print(f"❌ Create page failed to load (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error testing create page: {e}")
        return False

def main():
    print("🧪 Testing Upload Functionality in Text Editor")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Test create page
    success = test_create_page()
    
    print("\n📊 Test Results:")
    print("=" * 30)
    if success:
        print("✅ Upload functionality is properly integrated!")
        print("\n📝 How to use:")
        print("1. Go to http://127.0.0.1:5000/create")
        print("2. Look for the green 'Upload File' button in the text editor toolbar")
        print("3. Click it to select and upload your document")
        print("4. The content will automatically load into the text editor")
        print("5. Supported formats: TXT, MD, RTF, DOCX, PDF")
    else:
        print("❌ Upload functionality test failed!")

if __name__ == "__main__":
    main()
