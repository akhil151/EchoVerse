#!/usr/bin/env python3
"""
EchoVerse Colab URL Updater
This script helps you quickly update the Granite API URL when you restart Google Colab.
"""

import os
import re
import sys

def update_colab_url(new_url):
    """Update the Granite API URL in the .env file"""
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        return False
    
    # Read the current .env file
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Update the GRANITE_API_URL line
    pattern = r'GRANITE_API_URL=.*'
    replacement = f'GRANITE_API_URL={new_url}'
    
    updated_content = re.sub(pattern, replacement, content)
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated Granite API URL to: {new_url}")
    return True

def main():
    print("🚀 EchoVerse Colab URL Updater")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        new_url = sys.argv[1]
    else:
        print("📝 Please enter your new ngrok URL from Google Colab:")
        print("   Example: https://abc123-def456.ngrok-free.app")
        new_url = input("🔗 New URL: ").strip()
    
    if not new_url:
        print("❌ No URL provided!")
        return
    
    # Validate URL format
    if not new_url.startswith('https://') or 'ngrok' not in new_url:
        print("⚠️  Warning: This doesn't look like a valid ngrok URL")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Cancelled")
            return
    
    if update_colab_url(new_url):
        print("\n🎉 URL updated successfully!")
        print("💡 Now restart your Flask app to use the new URL:")
        print("   python app.py")
    else:
        print("❌ Failed to update URL")

if __name__ == "__main__":
    main()
