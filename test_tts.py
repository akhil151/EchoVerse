#!/usr/bin/env python3
"""
Test TTS Engine Functionality
"""

import os
import tempfile
from gtts import gTTS
from audio.professional_tts import ProfessionalTTSEngine

def test_gtts_directly():
    """Test gTTS directly"""
    try:
        print("🧪 Testing gTTS directly...")
        
        text = "Hello, this is a test of the Google Text-to-Speech engine."
        
        # Create TTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_path = temp_file.name
        temp_file.close()
        
        # Save audio
        tts.save(temp_path)
        
        # Check file
        if os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            print(f"✅ gTTS test successful! File: {temp_path} ({file_size} bytes)")
            
            # Clean up
            os.unlink(temp_path)
            return True
        else:
            print("❌ gTTS test failed - file not created")
            return False
            
    except Exception as e:
        print(f"❌ gTTS test failed: {e}")
        return False

def test_professional_tts():
    """Test Professional TTS Engine"""
    try:
        print("🎵 Testing Professional TTS Engine...")
        
        # Initialize engine
        tts_engine = ProfessionalTTSEngine()
        
        # Test text
        text = "This is a test of the professional TTS engine for EchoVerse."
        
        # Generate audio
        audio_file = tts_engine.generate_audio(
            text=text,
            language='en',
            voice_style='professional'
        )
        
        if audio_file and os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"✅ Professional TTS test successful! File: {audio_file} ({file_size} bytes)")
            
            # Clean up
            os.unlink(audio_file)
            return True
        else:
            print("❌ Professional TTS test failed - no audio file generated")
            return False
            
    except Exception as e:
        print(f"❌ Professional TTS test failed: {e}")
        return False

def test_audio_directory():
    """Test audio directory permissions"""
    try:
        print("📁 Testing audio directory...")
        
        # Ensure directory exists
        os.makedirs('static/audio', exist_ok=True)
        
        # Test write permissions
        test_file = 'static/audio/test_permissions.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        
        if os.path.exists(test_file):
            os.unlink(test_file)
            print("✅ Audio directory permissions OK")
            return True
        else:
            print("❌ Cannot write to audio directory")
            return False
            
    except Exception as e:
        print(f"❌ Audio directory test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 EchoVerse TTS Test Suite")
    print("=" * 40)
    
    # Test 1: Audio directory
    dir_ok = test_audio_directory()
    print()
    
    # Test 2: Direct gTTS
    gtts_ok = test_gtts_directly()
    print()
    
    # Test 3: Professional TTS
    if gtts_ok:
        prof_ok = test_professional_tts()
    else:
        prof_ok = False
        print("⏭️ Skipping Professional TTS test (gTTS failed)")
    
    print("\n📊 TTS Test Results")
    print("=" * 25)
    print(f"Directory Access: {'✅ PASS' if dir_ok else '❌ FAIL'}")
    print(f"Google TTS: {'✅ PASS' if gtts_ok else '❌ FAIL'}")
    print(f"Professional TTS: {'✅ PASS' if prof_ok else '❌ FAIL'}")
    
    if all([dir_ok, gtts_ok, prof_ok]):
        print("\n🎉 All TTS tests passed! Audio generation should work!")
    else:
        print("\n⚠️ Some TTS tests failed. This explains the 0:00 duration issue.")
        
        if not gtts_ok:
            print("\n💡 Suggestion: Check internet connection for Google TTS")
            print("   Alternative: Install offline TTS engines")
