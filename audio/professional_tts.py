"""
Professional Text-to-Speech Engine
==================================
Optimized TTS engine for professional audiobook creation.
Supports multiple languages, voice styles, and emotion-aware generation.
"""

import os
import logging
import tempfile
import uuid
from datetime import datetime
from gtts import gTTS
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ProfessionalTTSEngine:
    """
    Professional Text-to-Speech Engine for EchoVerse
    
    Features:
    - Multiple language support
    - Emotion-aware voice generation
    - Professional audio quality
    - Voice style adaptation
    - Batch processing capabilities
    """
    
    def __init__(self):
        """Initialize Professional TTS Engine"""
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
        
        self.voice_styles = {
            'neutral': {'speed': 1.0, 'pitch': 0},
            'dramatic': {'speed': 0.9, 'pitch': -2},
            'energetic': {'speed': 1.1, 'pitch': 2},
            'calm': {'speed': 0.8, 'pitch': -1},
            'professional': {'speed': 1.0, 'pitch': 0},
            'storytelling': {'speed': 0.95, 'pitch': 1}
        }
        
        # Ensure audio directory exists
        os.makedirs('static/audio', exist_ok=True)
        
        logger.info("Professional TTS Engine initialized")
    
    def generate_audio(self, text: str, language: str = 'en', 
                      emotion_data: Dict[str, Any] = None,
                      voice_style: str = 'neutral') -> Optional[str]:
        """
        Generate professional audio from text
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'es', 'fr')
            emotion_data: Emotion analysis data for voice adaptation
            voice_style: Voice style to use
            
        Returns:
            Path to generated audio file or None if failed
        """
        if not text or not text.strip():
            logger.error("Empty text provided for audio generation")
            return None
        
        try:
            logger.info(f"🎵 Generating audio: {len(text)} chars, {language} language, {voice_style} style")
            
            # Validate language
            if language not in self.supported_languages:
                logger.warning(f"Unsupported language '{language}', using English")
                language = 'en'
            
            # Adapt voice based on emotion data
            if emotion_data:
                voice_style = self._adapt_voice_for_emotion(emotion_data, voice_style)
            
            # Generate unique filename
            audio_id = str(uuid.uuid4())
            audio_filename = f"audiobook_{audio_id}.mp3"
            audio_path = os.path.join('static/audio', audio_filename)
            
            # Process text for better speech
            processed_text = self._preprocess_text(text)
            
            # Generate audio using gTTS
            tts = gTTS(
                text=processed_text,
                lang=language,
                slow=False
            )
            
            # Save audio file
            tts.save(audio_path)

            # Validate audio file was created and has content
            if not os.path.exists(audio_path):
                raise Exception(f"Audio file was not created: {audio_path}")

            file_size = os.path.getsize(audio_path)
            if file_size == 0:
                raise Exception(f"Audio file is empty: {audio_path}")

            logger.info(f"✅ Audio file validated: {audio_filename} ({file_size} bytes)")

            # Apply voice style modifications (if needed)
            if voice_style != 'neutral':
                audio_path = self._apply_voice_style(audio_path, voice_style)

            logger.info(f"✅ Audio generated successfully: {audio_filename}")
            return audio_path
            
        except Exception as e:
            logger.error(f"❌ Error generating audio: {str(e)}")
            return None
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better speech synthesis
        
        Args:
            text: Raw text
            
        Returns:
            Processed text optimized for TTS
        """
        # Remove excessive whitespace
        processed = ' '.join(text.split())
        
        # Add pauses for better pacing
        processed = processed.replace('.', '. ')
        processed = processed.replace(',', ', ')
        processed = processed.replace(';', '; ')
        processed = processed.replace(':', ': ')
        
        # Handle abbreviations
        abbreviations = {
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Missus',
            'Ms.': 'Miss',
            'Prof.': 'Professor',
            'St.': 'Saint',
            'Ave.': 'Avenue',
            'Rd.': 'Road',
            'Blvd.': 'Boulevard'
        }
        
        for abbrev, full_form in abbreviations.items():
            processed = processed.replace(abbrev, full_form)
        
        # Handle numbers (basic)
        processed = processed.replace('1st', 'first')
        processed = processed.replace('2nd', 'second')
        processed = processed.replace('3rd', 'third')
        
        return processed
    
    def _adapt_voice_for_emotion(self, emotion_data: Dict[str, Any], 
                                current_style: str) -> str:
        """
        Adapt voice style based on emotion analysis
        
        Args:
            emotion_data: Emotion analysis results
            current_style: Current voice style
            
        Returns:
            Adapted voice style
        """
        primary_emotion = emotion_data.get('primary', 'neutral')
        intensity = emotion_data.get('intensity', 0.5)
        
        # Map emotions to voice styles
        emotion_style_mapping = {
            'joy': 'energetic',
            'excitement': 'energetic',
            'sadness': 'calm',
            'fear': 'dramatic',
            'anger': 'dramatic',
            'surprise': 'energetic',
            'calm': 'calm',
            'neutral': 'neutral'
        }
        
        # Get recommended style based on emotion
        recommended_style = emotion_style_mapping.get(primary_emotion, current_style)
        
        # Use recommended style if intensity is high enough
        if intensity > 0.6:
            return recommended_style
        else:
            return current_style
    
    def _apply_voice_style(self, audio_path: str, style: str) -> str:
        """
        Apply voice style modifications to audio
        
        Args:
            audio_path: Path to audio file
            style: Voice style to apply
            
        Returns:
            Path to modified audio file
        """
        # For now, return original path
        # In a full implementation, you would use audio processing libraries
        # to modify speed, pitch, etc.
        logger.info(f"Voice style '{style}' would be applied to audio")
        return audio_path
    
    def generate_batch_audio(self, texts: list, language: str = 'en',
                           voice_style: str = 'neutral') -> list:
        """
        Generate audio for multiple texts
        
        Args:
            texts: List of texts to convert
            language: Language code
            voice_style: Voice style to use
            
        Returns:
            List of audio file paths
        """
        audio_files = []
        
        for i, text in enumerate(texts):
            logger.info(f"🎵 Processing batch item {i+1}/{len(texts)}")
            
            audio_file = self.generate_audio(
                text=text,
                language=language,
                voice_style=voice_style
            )
            
            if audio_file:
                audio_files.append(audio_file)
            else:
                logger.warning(f"Failed to generate audio for batch item {i+1}")
        
        logger.info(f"✅ Batch processing complete: {len(audio_files)}/{len(texts)} successful")
        return audio_files
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported languages"""
        return self.supported_languages.copy()
    
    def get_voice_styles(self) -> list:
        """Get list of available voice styles"""
        return list(self.voice_styles.keys())
    
    def estimate_audio_duration(self, text: str, language: str = 'en') -> float:
        """
        Estimate audio duration in minutes
        
        Args:
            text: Text to analyze
            language: Language code
            
        Returns:
            Estimated duration in minutes
        """
        word_count = len(text.split())
        
        # Average speaking rates by language (words per minute)
        speaking_rates = {
            'en': 150,  # English
            'es': 160,  # Spanish
            'fr': 140,  # French
            'de': 130,  # German
            'it': 155,  # Italian
            'pt': 150,  # Portuguese
            'ru': 135,  # Russian
            'ja': 120,  # Japanese
            'ko': 125,  # Korean
            'zh': 110,  # Chinese
            'ar': 140,  # Arabic
            'hi': 145   # Hindi
        }
        
        rate = speaking_rates.get(language, 150)
        duration_minutes = word_count / rate
        
        return round(duration_minutes, 1)
    
    def get_audio_info(self, audio_path: str) -> Dict[str, Any]:
        """
        Get information about generated audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Audio file information
        """
        if not os.path.exists(audio_path):
            return {'error': 'Audio file not found'}
        
        file_size = os.path.getsize(audio_path)
        file_stats = os.stat(audio_path)
        
        return {
            'file_path': audio_path,
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'created_at': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            'format': 'MP3',
            'quality': 'Standard'
        }
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Clean up old audio files
        
        Args:
            max_age_hours: Maximum age of files to keep (in hours)
        """
        try:
            audio_dir = 'static/audio'
            if not os.path.exists(audio_dir):
                return
            
            current_time = datetime.now().timestamp()
            max_age_seconds = max_age_hours * 3600
            
            cleaned_count = 0
            
            for filename in os.listdir(audio_dir):
                file_path = os.path.join(audio_dir, filename)
                
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"🧹 Cleaned up {cleaned_count} old audio files")
            
        except Exception as e:
            logger.error(f"Error cleaning up audio files: {str(e)}")
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get TTS engine status"""
        return {
            'status': 'ready',
            'supported_languages': len(self.supported_languages),
            'voice_styles': len(self.voice_styles),
            'audio_directory': 'static/audio',
            'engine_type': 'gTTS (Google Text-to-Speech)'
        }
