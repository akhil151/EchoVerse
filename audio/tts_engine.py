"""
Advanced Text-to-Speech Engine
===============================
Professional TTS engine with emotion-aware voice synthesis,
multiple language support, and advanced audio processing.
"""

import os
import tempfile
import logging
from gtts import gTTS
import pyttsx3
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class AdvancedTTSEngine:
    """
    Advanced Text-to-Speech Engine for EchoVerse
    
    Features:
    - Emotion-aware voice synthesis
    - Multiple TTS backends (gTTS, pyttsx3, future: Coqui TTS)
    - Voice style adaptation
    - Speed and pitch control
    - Multi-language support
    - Audio quality optimization
    """
    
    def __init__(self):
        """Initialize the advanced TTS engine"""
        self.supported_languages = {
            'en': {'name': 'English', 'gtts_code': 'en', 'pyttsx3_voice': 'english'},
            'es': {'name': 'Spanish', 'gtts_code': 'es', 'pyttsx3_voice': 'spanish'},
            'fr': {'name': 'French', 'gtts_code': 'fr', 'pyttsx3_voice': 'french'},
            'de': {'name': 'German', 'gtts_code': 'de', 'pyttsx3_voice': 'german'},
            'it': {'name': 'Italian', 'gtts_code': 'it', 'pyttsx3_voice': 'italian'},
            'pt': {'name': 'Portuguese', 'gtts_code': 'pt', 'pyttsx3_voice': 'portuguese'},
            'ru': {'name': 'Russian', 'gtts_code': 'ru', 'pyttsx3_voice': 'russian'},
            'ja': {'name': 'Japanese', 'gtts_code': 'ja', 'pyttsx3_voice': 'japanese'},
            'ko': {'name': 'Korean', 'gtts_code': 'ko', 'pyttsx3_voice': 'korean'},
            'zh': {'name': 'Chinese', 'gtts_code': 'zh', 'pyttsx3_voice': 'chinese'},
            'ar': {'name': 'Arabic', 'gtts_code': 'ar', 'pyttsx3_voice': 'arabic'},
            'hi': {'name': 'Hindi', 'gtts_code': 'hi', 'pyttsx3_voice': 'hindi'}
        }
        
        # Voice style configurations
        self.voice_styles = {
            "natural": {"speed": 1.0, "pitch": 0, "volume": 0.9},
            "upbeat": {"speed": 1.1, "pitch": 2, "volume": 1.0},
            "gentle": {"speed": 0.85, "pitch": -1, "volume": 0.8},
            "dramatic": {"speed": 0.95, "pitch": 1, "volume": 0.95},
            "energetic": {"speed": 1.15, "pitch": 3, "volume": 1.0},
            "soothing": {"speed": 0.8, "pitch": -2, "volume": 0.75},
            "neutral": {"speed": 1.0, "pitch": 0, "volume": 0.9}
        }
        
        # Emotion-based adjustments
        self.emotion_adjustments = {
            "joy": {"speed_mult": 1.1, "pitch_add": 2, "volume_mult": 1.0},
            "sadness": {"speed_mult": 0.85, "pitch_add": -2, "volume_mult": 0.8},
            "fear": {"speed_mult": 0.9, "pitch_add": 1, "volume_mult": 0.9},
            "excitement": {"speed_mult": 1.15, "pitch_add": 3, "volume_mult": 1.0},
            "calm": {"speed_mult": 0.9, "pitch_add": -1, "volume_mult": 0.8},
            "anger": {"speed_mult": 1.05, "pitch_add": 2, "volume_mult": 0.95},
            "neutral": {"speed_mult": 1.0, "pitch_add": 0, "volume_mult": 0.9}
        }
        
        # Initialize pyttsx3 engine (with Python 3.13 compatibility check)
        try:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_available = True
            logger.info("pyttsx3 TTS engine initialized")
        except Exception as e:
            self.pyttsx3_engine = None
            self.pyttsx3_available = False
            logger.warning(f"pyttsx3 not available (Python 3.13 compatibility issue): {str(e)}")
            logger.info("Using gTTS as primary TTS engine")
        
        logger.info("Advanced TTS Engine initialized")
    
    def generate_audio(self, text, language='en', emotion_data=None, voice_style='natural', backend='gtts'):
        """
        Generate audio from text with emotion-aware synthesis
        
        Args:
            text: Text to convert to speech
            language: Language code
            emotion_data: Emotion analysis data from Mistral model
            voice_style: Voice style preference
            backend: TTS backend to use ('gtts', 'pyttsx3')
            
        Returns:
            Path to generated audio file
        """
        if not text or not text.strip():
            return None
        
        try:
            # Determine optimal voice settings
            voice_config = self._get_voice_config(emotion_data, voice_style)
            
            # Choose backend based on availability and requirements
            if backend == 'pyttsx3' and self.pyttsx3_available:
                audio_file = self._generate_with_pyttsx3(text, language, voice_config)
            else:
                audio_file = self._generate_with_gtts(text, language, voice_config)
            
            logger.info(f"Audio generated successfully: {audio_file}")
            return audio_file
            
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            return None
    
    def _get_voice_config(self, emotion_data, voice_style):
        """
        Calculate optimal voice configuration based on emotion and style
        
        Args:
            emotion_data: Emotion analysis from Mistral model
            voice_style: Requested voice style
            
        Returns:
            Voice configuration dictionary
        """
        # Start with base style configuration
        config = self.voice_styles.get(voice_style, self.voice_styles['natural']).copy()
        
        # Apply emotion-based adjustments if available
        if emotion_data and 'primary_emotion' in emotion_data:
            primary_emotion = emotion_data['primary_emotion']
            intensity = emotion_data.get('intensity', 0.5)
            
            if primary_emotion in self.emotion_adjustments:
                emotion_adj = self.emotion_adjustments[primary_emotion]
                
                # Apply adjustments with intensity scaling
                config['speed'] *= (1 + (emotion_adj['speed_mult'] - 1) * intensity)
                config['pitch'] += emotion_adj['pitch_add'] * intensity
                config['volume'] *= (1 + (emotion_adj['volume_mult'] - 1) * intensity)
        
        # Ensure values are within reasonable bounds
        config['speed'] = max(0.5, min(2.0, config['speed']))
        config['pitch'] = max(-10, min(10, config['pitch']))
        config['volume'] = max(0.1, min(1.0, config['volume']))
        
        return config
    
    def _generate_with_gtts(self, text, language, voice_config):
        """
        Generate audio using Google Text-to-Speech
        
        Args:
            text: Text to synthesize
            language: Language code
            voice_config: Voice configuration
            
        Returns:
            Path to generated audio file
        """
        try:
            # Get language configuration
            lang_config = self.supported_languages.get(language, self.supported_languages['en'])
            gtts_lang = lang_config['gtts_code']
            
            # Adjust speech speed through text modification if needed
            slow_speech = voice_config['speed'] < 0.9
            
            # Generate TTS
            tts = gTTS(
                text=text,
                lang=gtts_lang,
                slow=slow_speech,
                tld='com'  # Use .com domain for better quality
            )
            
            # Create temporary file
            audio_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=".mp3",
                dir="static/audio"
            )
            
            tts.save(audio_file.name)
            
            return audio_file.name
            
        except Exception as e:
            logger.error(f"Error with gTTS: {str(e)}")
            raise
    
    def _generate_with_pyttsx3(self, text, language, voice_config):
        """
        Generate audio using pyttsx3 (offline TTS)
        
        Args:
            text: Text to synthesize
            language: Language code
            voice_config: Voice configuration
            
        Returns:
            Path to generated audio file
        """
        try:
            if not self.pyttsx3_available:
                raise Exception("pyttsx3 not available")
            
            # Configure voice properties
            self.pyttsx3_engine.setProperty('rate', int(200 * voice_config['speed']))
            self.pyttsx3_engine.setProperty('volume', voice_config['volume'])
            
            # Try to set voice based on language (if available)
            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                # Simple voice selection (could be improved)
                voice_id = 0 if language == 'en' else min(1, len(voices) - 1)
                self.pyttsx3_engine.setProperty('voice', voices[voice_id].id)
            
            # Create temporary file
            audio_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav",
                dir="static/audio"
            )
            
            # Generate audio
            self.pyttsx3_engine.save_to_file(text, audio_file.name)
            self.pyttsx3_engine.runAndWait()
            
            return audio_file.name
            
        except Exception as e:
            logger.error(f"Error with pyttsx3: {str(e)}")
            raise
    
    def generate_preview(self, text, language='en', max_length=100):
        """
        Generate a short preview of the audio
        
        Args:
            text: Full text
            language: Language code
            max_length: Maximum characters for preview
            
        Returns:
            Path to preview audio file
        """
        # Create preview text
        preview_text = text[:max_length]
        if len(text) > max_length:
            # Try to end at a sentence boundary
            last_period = preview_text.rfind('.')
            if last_period > max_length // 2:
                preview_text = preview_text[:last_period + 1]
            else:
                preview_text += "..."
        
        return self.generate_audio(preview_text, language=language)
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return {
            code: info['name'] 
            for code, info in self.supported_languages.items()
        }
    
    def get_voice_styles(self):
        """Get available voice styles"""
        return list(self.voice_styles.keys())
    
    def estimate_duration(self, text, voice_config=None):
        """
        Estimate audio duration in seconds
        
        Args:
            text: Input text
            voice_config: Voice configuration (optional)
            
        Returns:
            Estimated duration in seconds
        """
        if not voice_config:
            voice_config = self.voice_styles['natural']
        
        # Rough estimation: average speaking rate is ~150 words per minute
        word_count = len(text.split())
        base_duration = (word_count / 150) * 60  # seconds
        
        # Adjust for speed
        adjusted_duration = base_duration / voice_config['speed']
        
        return round(adjusted_duration, 1)
    
    def get_engine_info(self):
        """Get TTS engine information"""
        return {
            "backends": {
                "gtts": True,
                "pyttsx3": self.pyttsx3_available
            },
            "supported_languages": len(self.supported_languages),
            "voice_styles": len(self.voice_styles),
            "emotion_support": True
        }
