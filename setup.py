#!/usr/bin/env python3
"""
EchoVerse Professional Setup Script
===================================
Automated setup for the EchoVerse AI Audiobook Platform
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("=" * 60)
    print("🎬 EchoVerse Professional AI Audiobook Platform")
    print("=" * 60)
    print("🚀 Setting up your professional audiobook creation platform...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = [
        "static/audio",
        "uploads",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def check_env_file():
    """Check if .env file exists and is configured"""
    print("\n🔧 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("📝 Please copy .env.example to .env and configure your API keys")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'your_groq_api_key_here' in content or 'your_huggingface_token_here' in content:
        print("⚠️  .env file found but not configured")
        print("📝 Please update your API keys in .env file")
        return False
    
    print("✅ Environment file configured")
    return True

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check environment configuration
    env_configured = check_env_file()
    
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    
    if env_configured:
        print("✅ Your EchoVerse platform is ready to run!")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("⚠️  Setup complete but configuration needed:")
        print("1. Configure your API keys in .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    
    print("\n📚 For help, see README.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
