#!/usr/bin/env python3
"""
EchoVerse Professional Startup Script
=====================================
Complete startup script for EchoVerse AI Audiobook Creation Platform.
Handles initialization, validation, and startup of all services.
"""

import os
import sys
import logging
import subprocess
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EchoVerseStarter:
    """Professional startup manager for EchoVerse"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.required_dirs = [
            'static/audio',
            'uploads',
            'temp',
            'logs'
        ]
        self.required_files = [
            '.env',
            'app.py',
            'requirements.txt'
        ]
    
    def validate_environment(self):
        """Validate the environment and dependencies"""
        logger.info("🔍 Validating EchoVerse environment...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("❌ Python 3.8+ required")
            return False
        
        logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        
        # Check required files
        for file_path in self.required_files:
            if not (self.project_root / file_path).exists():
                logger.error(f"❌ Required file missing: {file_path}")
                return False
        
        logger.info("✅ All required files present")
        
        # Create required directories
        for dir_path in self.required_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Directory ready: {dir_path}")
        
        return True
    
    def check_dependencies(self):
        """Check if required Python packages are installed"""
        logger.info("📦 Checking Python dependencies...")
        
        required_packages = [
            'flask',
            'requests',
            'gtts',
            'python-dotenv'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✅ {package} installed")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"⚠️ {package} not installed")
        
        if missing_packages:
            logger.info("📥 Installing missing packages...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install'
                ] + missing_packages)
                logger.info("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError:
                logger.error("❌ Failed to install dependencies")
                return False
        
        return True
    
    def validate_configuration(self):
        """Validate .env configuration"""
        logger.info("⚙️ Validating configuration...")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check critical environment variables
        granite_url = os.getenv('GRANITE_API_URL')
        if not granite_url or granite_url == 'your_granite_url_here':
            logger.warning("⚠️ GRANITE_API_URL not configured properly")
            logger.info("💡 Please update your .env file with the correct Granite API URL from Google Colab")
        else:
            logger.info(f"✅ Granite API URL configured: {granite_url}")
        
        secret_key = os.getenv('SECRET_KEY')
        if secret_key:
            logger.info("✅ Secret key configured")
        else:
            logger.warning("⚠️ SECRET_KEY not set, using default")
        
        return True
    
    def test_services(self):
        """Test critical services"""
        logger.info("🧪 Testing services...")
        
        # Test TTS
        try:
            from gtts import gTTS
            test_tts = gTTS(text="Test", lang='en')
            logger.info("✅ Google TTS service available")
        except Exception as e:
            logger.error(f"❌ TTS service error: {e}")
            return False
        
        # Test Granite connection (if configured)
        granite_url = os.getenv('GRANITE_API_URL')
        if granite_url and granite_url != 'your_granite_url_here':
            try:
                import requests
                response = requests.get(f"{granite_url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Granite API connection successful")
                else:
                    logger.warning("⚠️ Granite API not responding properly")
            except Exception as e:
                logger.warning(f"⚠️ Granite API connection failed: {e}")
        
        return True
    
    def start_application(self):
        """Start the EchoVerse application"""
        logger.info("🚀 Starting EchoVerse Professional Platform...")
        
        try:
            # Import and run the Flask app
            from app import app
            
            logger.info("✅ EchoVerse initialized successfully!")
            logger.info("🌐 Starting web server...")
            logger.info("📱 Access EchoVerse at: http://127.0.0.1:5000")
            logger.info("🎵 Create audiobooks at: http://127.0.0.1:5000/create")
            logger.info("⭐ View features at: http://127.0.0.1:5000/features")
            
            # Start Flask app
            app.run(
                host='0.0.0.0',
                port=5000,
                debug=True,
                threaded=True
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to start application: {e}")
            return False
        
        return True
    
    def run(self):
        """Run the complete startup process"""
        logger.info("🎬 EchoVerse Professional Startup")
        logger.info("=" * 50)
        
        # Step 1: Validate environment
        if not self.validate_environment():
            logger.error("❌ Environment validation failed")
            return False
        
        # Step 2: Check dependencies
        if not self.check_dependencies():
            logger.error("❌ Dependency check failed")
            return False
        
        # Step 3: Validate configuration
        if not self.validate_configuration():
            logger.error("❌ Configuration validation failed")
            return False
        
        # Step 4: Test services
        if not self.test_services():
            logger.error("❌ Service testing failed")
            return False
        
        # Step 5: Start application
        logger.info("🎉 All checks passed! Starting EchoVerse...")
        return self.start_application()

def main():
    """Main entry point"""
    starter = EchoVerseStarter()
    success = starter.run()
    
    if not success:
        logger.error("❌ EchoVerse startup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
