"""
IBM Granite API Client
======================
Professional client for connecting to IBM Granite model hosted on Google Colab.
Handles text transformation with various tones and styles.
"""

import requests
import logging
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class GraniteAPIClient:
    """
    Professional client for IBM Granite model API
    
    Connects to IBM Granite model hosted on Google Colab via ngrok tunnel.
    Provides text transformation capabilities with multiple tones.
    """
    
    def __init__(self, api_url: str):
        """
        Initialize Granite API client
        
        Args:
            api_url: Base URL of the Granite API (from Google Colab ngrok)
        """
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
        
        # Available tones
        self.available_tones = [
            'neutral', 'suspenseful', 'dramatic', 'inspiring',
            'educational', 'conversational', 'formal', 'calming'
        ]
        
        logger.info(f"Granite API Client initialized with URL: {self.api_url}")
    
    def test_connection(self) -> bool:
        """
        Test connection to Granite API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Granite API connection successful: {data.get('message', 'OK')}")
                return True
            else:
                logger.error(f"❌ Granite API health check failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Granite API connection failed: {str(e)}")
            return False
    
    def get_available_tones(self) -> list:
        """
        Get list of available tones from API
        
        Returns:
            List of available tones
        """
        try:
            response = self.session.get(f"{self.api_url}/available-tones", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('tones', self.available_tones)
            else:
                logger.warning("Failed to fetch tones from API, using defaults")
                return self.available_tones
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching tones: {str(e)}, using defaults")
            return self.available_tones
    
    def transform_text(self, text: str, tone: str = 'neutral') -> str:
        """
        Transform text using IBM Granite model
        
        Args:
            text: Input text to transform
            tone: Desired tone for transformation
            
        Returns:
            Transformed text
        """
        if not text or not text.strip():
            return text
        
        # Validate tone
        if tone not in self.available_tones:
            logger.warning(f"Unknown tone '{tone}', using 'neutral'")
            tone = 'neutral'
        
        try:
            logger.info(f"🔄 Transforming text with tone: {tone}")
            
            # Prepare request
            payload = {
                'text': text,
                'tone': tone
            }
            
            # Make API request
            response = self.session.post(
                f"{self.api_url}/transform",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    transformed_text = data.get('transformed_text', text)
                    logger.info("✅ Text transformation successful")
                    return transformed_text
                else:
                    logger.error(f"API returned error: {data.get('error', 'Unknown error')}")
                    return self._fallback_transform(text, tone)
            else:
                logger.error(f"API request failed: {response.status_code}")
                return self._fallback_transform(text, tone)
                
        except requests.exceptions.Timeout:
            logger.error("⏰ Granite API request timed out")
            return self._fallback_transform(text, tone)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Granite API request failed: {str(e)}")
            return self._fallback_transform(text, tone)
        
        except Exception as e:
            logger.error(f"❌ Unexpected error in text transformation: {str(e)}")
            return self._fallback_transform(text, tone)
    
    def _fallback_transform(self, text: str, tone: str) -> str:
        """
        Fallback text transformation when API is unavailable
        
        Args:
            text: Input text
            tone: Desired tone
            
        Returns:
            Transformed text using local rules
        """
        logger.info(f"🔄 Using fallback transformation for tone: {tone}")
        
        # Simple tone-based transformations
        transformations = {
            'suspenseful': {
                'prefix': 'In a spine-chilling turn of events, ',
                'suffix': ' The tension was palpable, leaving everyone on edge.',
                'replacements': {
                    'walked': 'crept cautiously',
                    'said': 'whispered ominously',
                    'looked': 'peered suspiciously',
                    'went': 'ventured carefully'
                }
            },
            'dramatic': {
                'prefix': 'With overwhelming emotion, ',
                'suffix': ' The moment was filled with raw, powerful intensity.',
                'replacements': {
                    'walked': 'strode dramatically',
                    'said': 'declared passionately',
                    'looked': 'gazed intensely',
                    'felt': 'experienced deeply'
                }
            },
            'inspiring': {
                'prefix': 'With hope and determination, ',
                'suffix': ' This moment would inspire generations to come.',
                'replacements': {
                    'walked': 'moved forward courageously',
                    'said': 'proclaimed with conviction',
                    'looked': 'envisioned a brighter future',
                    'tried': 'persevered with unwavering resolve'
                }
            },
            'calming': {
                'prefix': 'In peaceful serenity, ',
                'suffix': ' A sense of tranquil calm settled over everything.',
                'replacements': {
                    'walked': 'strolled peacefully',
                    'said': 'spoke gently',
                    'looked': 'observed serenely',
                    'moved': 'flowed gracefully'
                }
            },
            'educational': {
                'prefix': 'It is important to understand that ',
                'suffix': ' This knowledge forms the foundation for further learning.',
                'replacements': {
                    'said': 'explained clearly',
                    'showed': 'demonstrated effectively',
                    'found': 'discovered through research',
                    'knew': 'understood from evidence'
                }
            },
            'formal': {
                'prefix': 'It should be noted that ',
                'suffix': ' This matter requires careful consideration.',
                'replacements': {
                    'said': 'stated formally',
                    'told': 'informed officially',
                    'asked': 'inquired respectfully',
                    'got': 'obtained through proper channels'
                }
            },
            'conversational': {
                'prefix': 'You know, ',
                'suffix': ' Pretty interesting stuff, right?',
                'replacements': {
                    'said': 'mentioned casually',
                    'told': 'shared with me',
                    'found': 'came across',
                    'learned': 'picked up'
                }
            }
        }
        
        if tone in transformations:
            transform = transformations[tone]
            result = text
            
            # Apply word replacements
            for old_word, new_word in transform['replacements'].items():
                result = result.replace(old_word, new_word)
                result = result.replace(old_word.capitalize(), new_word.capitalize())
            
            # Add prefix and suffix for shorter texts
            if len(result.split()) < 50:
                result = transform['prefix'] + result + transform['suffix']
            
            return result
        
        # Return original text for neutral or unknown tones
        return text
    
    def batch_transform(self, texts: list, tone: str = 'neutral') -> list:
        """
        Transform multiple texts in batch
        
        Args:
            texts: List of texts to transform
            tone: Desired tone for all transformations
            
        Returns:
            List of transformed texts
        """
        results = []
        
        for i, text in enumerate(texts):
            logger.info(f"🔄 Transforming text {i+1}/{len(texts)}")
            transformed = self.transform_text(text, tone)
            results.append(transformed)
            
            # Small delay to avoid overwhelming the API
            if i < len(texts) - 1:
                time.sleep(0.5)
        
        return results
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Get detailed API status information
        
        Returns:
            Dictionary with API status details
        """
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=10)
            
            if response.status_code == 200:
                return {
                    'status': 'online',
                    'response_time': response.elapsed.total_seconds(),
                    'details': response.json()
                }
            else:
                return {
                    'status': 'error',
                    'response_time': response.elapsed.total_seconds(),
                    'error_code': response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'status': 'offline',
                'error': str(e)
            }
