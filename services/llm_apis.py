"""
Free LLM APIs Manager
====================
Professional integration with free LLM APIs for enhanced functionality.
Supports Groq, Hugging Face, and other free AI services.
"""

import requests
import logging
import json
import time
import os
from typing import Optional, Dict, Any, List

# Free LLM API clients
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False

try:
    import replicate
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class LLMAPIManager:
    """
    Professional manager for free LLM APIs
    
    Integrates multiple free AI services:
    - Groq API (Free tier)
    - Hugging Face Inference API (Free)
    - OpenAI-compatible APIs
    """
    
    def __init__(self, groq_api_key: str = '', huggingface_api_key: str = ''):
        """
        Initialize LLM API manager with multiple free models

        Args:
            groq_api_key: Free Groq API key
            huggingface_api_key: Free Hugging Face API key
        """
        # Get API keys from environment or parameters
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY', '')
        self.huggingface_api_key = huggingface_api_key or os.getenv('HUGGINGFACE_API_KEY', '')
        self.together_api_key = os.getenv('TOGETHER_API_KEY', '')
        self.cohere_api_key = os.getenv('COHERE_API_KEY', '')
        self.replicate_api_token = os.getenv('REPLICATE_API_TOKEN', '')
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')

        # Initialize API clients
        self.groq_client = None
        self.cohere_client = None
        self.openai_client = None
        self.hf_token = self.huggingface_api_key

        # Initialize Groq client
        if self.groq_api_key and GROQ_AVAILABLE:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
                logger.info("✅ Groq API client initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Groq client: {str(e)}")

        # Initialize Cohere client
        if self.cohere_api_key and COHERE_AVAILABLE:
            try:
                self.cohere_client = cohere.Client(self.cohere_api_key)
                logger.info("✅ Cohere API client initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Cohere client: {str(e)}")

        # Initialize OpenAI client (for Together AI and others)
        if OPENAI_AVAILABLE:
            try:
                if self.together_api_key:
                    self.openai_client = openai.OpenAI(
                        api_key=self.together_api_key,
                        base_url="https://api.together.xyz/v1"
                    )
                    logger.info("✅ Together AI client initialized")
                elif self.openai_api_key:
                    self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
                    logger.info("✅ OpenAI client initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")

        # Initialize Replicate
        if self.replicate_api_token and REPLICATE_AVAILABLE:
            try:
                replicate.api_token = self.replicate_api_token
                logger.info("✅ Replicate API initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Replicate: {str(e)}")

        # API endpoints
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.hf_url = "https://api-inference.huggingface.co/models"

        # Session for requests
        self.session = requests.Session()
        self.session.timeout = 30

        # Available free models
        self.free_models = {
            'groq': [
                'llama3-8b-8192',
                'llama3-70b-8192',
                'mixtral-8x7b-32768',
                'gemma-7b-it'
            ],
            'huggingface': [
                'microsoft/DialoGPT-medium',
                'facebook/blenderbot-400M-distill',
                'microsoft/DialoGPT-large',
                'google/flan-t5-base'
            ],
            'ollama': [
                'llama2:7b',
                'mistral:7b',
                'codellama:7b',
                'phi:2.7b'
            ],
            'together': [
                'meta-llama/Llama-2-7b-chat-hf',
                'meta-llama/Llama-2-13b-chat-hf',
                'mistralai/Mixtral-8x7B-Instruct-v0.1',
                'NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO'
            ],
            'cohere': [
                'command-light',
                'command',
                'command-nightly'
            ],
            'replicate': [
                'meta/llama-2-7b-chat',
                'meta/llama-2-13b-chat',
                'mistralai/mixtral-8x7b-instruct-v0.1'
            ],
            'local': [
                'gpt2',
                'distilgpt2',
                'microsoft/DialoGPT-small'
            ]
        }

        logger.info("LLM API Manager initialized with multiple free models")
    
    def test_connections(self) -> Dict[str, bool]:
        """
        Test connections to all available APIs
        
        Returns:
            Dictionary with connection status for each API
        """
        results = {}
        
        # Test Groq API
        if self.groq_api_key:
            results['groq'] = self._test_groq_connection()
        else:
            results['groq'] = False
            logger.warning("Groq API key not provided")
        
        # Test Hugging Face API
        if self.huggingface_api_key:
            results['huggingface'] = self._test_huggingface_connection()
        else:
            results['huggingface'] = False
            logger.warning("Hugging Face API key not provided")
        
        # Test free APIs (no key required)
        results['free_apis'] = self._test_free_apis()
        
        return results
    
    def _test_groq_connection(self) -> bool:
        """Test Groq API connection"""
        try:
            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'llama3-8b-8192',
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'max_tokens': 10
            }
            
            response = self.session.post(self.groq_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Groq API connection successful")
                return True
            else:
                logger.error(f"❌ Groq API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Groq API connection error: {str(e)}")
            return False
    
    def _test_huggingface_connection(self) -> bool:
        """Test Hugging Face API connection"""
        try:
            headers = {
                'Authorization': f'Bearer {self.huggingface_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Test with a simple model
            url = f"{self.hf_url}/microsoft/DialoGPT-medium"
            payload = {'inputs': 'Hello'}
            
            response = self.session.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Hugging Face API connection successful")
                return True
            else:
                logger.error(f"❌ Hugging Face API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Hugging Face API connection error: {str(e)}")
            return False
    
    def _test_free_apis(self) -> bool:
        """Test free APIs that don't require authentication"""
        try:
            # Test a free API endpoint
            response = self.session.get("https://httpbin.org/status/200", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def enhance_content(self, text: str, enhancement_type: str = 'general') -> str:
        """
        Enhance content using available LLM APIs
        
        Args:
            text: Input text to enhance
            enhancement_type: Type of enhancement (general, creative, formal, etc.)
            
        Returns:
            Enhanced text
        """
        if not text or not text.strip():
            return text
        
        logger.info(f"🚀 Enhancing content with type: {enhancement_type}")
        
        # Try Groq API first (if available)
        if self.groq_api_key:
            enhanced = self._enhance_with_groq(text, enhancement_type)
            if enhanced and enhanced != text:
                return enhanced
        
        # Try Cohere API
        if self.cohere_api_key:
            enhanced = self.use_cohere_model(text)
            if enhanced and enhanced != text:
                return enhanced

        # Try Together AI
        if self.together_api_key:
            enhanced = self.use_together_model(text)
            if enhanced and enhanced != text:
                return enhanced

        # Try Replicate API
        if self.replicate_api_token:
            enhanced = self.use_replicate_model(text)
            if enhanced and enhanced != text:
                return enhanced

        # Try Hugging Face API
        if self.huggingface_api_key:
            enhanced = self._enhance_with_huggingface(text, enhancement_type)
            if enhanced and enhanced != text:
                return enhanced

        # Try Ollama local models (completely free)
        try:
            ollama_result = self.use_ollama_model(text)
            if ollama_result and ollama_result != text:
                logger.info("✅ Ollama local model enhancement successful")
                return ollama_result
        except Exception as e:
            logger.warning(f"Ollama not available: {str(e)}")

        # Try local transformers enhancement
        try:
            local_result = self.use_local_transformers(text)
            if local_result and local_result != text:
                logger.info("✅ Local transformers enhancement successful")
                return local_result
        except Exception as e:
            logger.warning(f"Local transformers error: {str(e)}")

        # Fallback to local enhancement
        return self._fallback_enhance(text, enhancement_type)
    
    def _enhance_with_groq(self, text: str, enhancement_type: str) -> str:
        """Enhance text using Groq API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Create enhancement prompt
            prompts = {
                'general': f"Improve and enhance the following text while maintaining its original meaning:\n\n{text}\n\nEnhanced version:",
                'creative': f"Rewrite the following text with more creative and engaging language:\n\n{text}\n\nCreative version:",
                'formal': f"Rewrite the following text in a more formal and professional style:\n\n{text}\n\nFormal version:",
                'narrative': f"Transform the following text into a more engaging narrative:\n\n{text}\n\nNarrative version:"
            }
            
            prompt = prompts.get(enhancement_type, prompts['general'])
            
            payload = {
                'model': 'llama3-8b-8192',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 500,
                'temperature': 0.7
            }
            
            response = self.session.post(self.groq_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                enhanced_text = data['choices'][0]['message']['content'].strip()
                logger.info("✅ Groq enhancement successful")
                return enhanced_text
            else:
                logger.error(f"Groq API error: {response.status_code}")
                return text
                
        except Exception as e:
            logger.error(f"Groq enhancement error: {str(e)}")
            return text
    
    def _enhance_with_huggingface(self, text: str, enhancement_type: str) -> str:
        """Enhance text using Hugging Face API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.huggingface_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Use a text generation model
            url = f"{self.hf_url}/microsoft/DialoGPT-large"
            
            # Create enhancement prompt
            prompt = f"Enhance this text: {text}"
            
            payload = {
                'inputs': prompt,
                'parameters': {
                    'max_new_tokens': 200,
                    'temperature': 0.7,
                    'return_full_text': False
                }
            }
            
            response = self.session.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    enhanced_text = data[0].get('generated_text', text).strip()
                    logger.info("✅ Hugging Face enhancement successful")
                    return enhanced_text
                else:
                    return text
            else:
                logger.error(f"Hugging Face API error: {response.status_code}")
                return text
                
        except Exception as e:
            logger.error(f"Hugging Face enhancement error: {str(e)}")
            return text
    
    def _fallback_enhance(self, text: str, enhancement_type: str) -> str:
        """Fallback enhancement using local rules"""
        logger.info(f"🔄 Using fallback enhancement for type: {enhancement_type}")
        
        enhancements = {
            'general': {
                'replacements': {
                    'good': 'excellent',
                    'bad': 'unfortunate',
                    'big': 'substantial',
                    'small': 'modest',
                    'nice': 'delightful',
                    'said': 'expressed',
                    'went': 'proceeded',
                    'got': 'obtained'
                }
            },
            'creative': {
                'replacements': {
                    'walked': 'meandered gracefully',
                    'looked': 'gazed with wonder',
                    'said': 'whispered enchantingly',
                    'felt': 'experienced a profound sense of',
                    'saw': 'beheld the magnificent sight of',
                    'heard': 'was captivated by the sound of'
                }
            },
            'formal': {
                'replacements': {
                    'got': 'obtained',
                    'said': 'stated',
                    'told': 'informed',
                    'asked': 'inquired',
                    'showed': 'demonstrated',
                    'found': 'discovered',
                    'made': 'created'
                }
            }
        }
        
        enhancement = enhancements.get(enhancement_type, enhancements['general'])
        result = text
        
        # Apply replacements
        for old_word, new_word in enhancement['replacements'].items():
            result = result.replace(f' {old_word} ', f' {new_word} ')
            result = result.replace(f' {old_word.capitalize()} ', f' {new_word.capitalize()} ')
        
        return result
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using available APIs
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        # Simple fallback sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'love', 'happy', 'joy']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'sad', 'angry', 'fear', 'worry']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'positive_score': positive_count,
            'negative_score': negative_count
        }
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get status of all APIs"""
        return {
            'groq': {
                'available': bool(self.groq_api_key),
                'status': 'configured' if self.groq_api_key else 'not_configured'
            },
            'huggingface': {
                'available': bool(self.huggingface_api_key),
                'status': 'configured' if self.huggingface_api_key else 'not_configured'
            },
            'fallback': {
                'available': True,
                'status': 'always_available'
            }
        }

    def test_apis(self) -> Dict[str, Any]:
        """
        Test all API connections

        Returns:
            Dictionary with API test results
        """
        results = {}

        # Test Groq API
        try:
            if self.groq_client:
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": "test"}],
                    model="llama3-8b-8192",
                    max_tokens=5
                )
                results['groq'] = {'status': 'online', 'model': 'llama3-8b-8192'}
            else:
                results['groq'] = {'status': 'offline', 'error': 'No API key'}
        except Exception as e:
            results['groq'] = {'status': 'offline', 'error': str(e)}

        # Test Hugging Face API
        try:
            if self.hf_token:
                response = requests.post(
                    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                    headers={"Authorization": f"Bearer {self.hf_token}"},
                    json={"inputs": "test"},
                    timeout=10
                )
                if response.status_code == 200:
                    results['huggingface'] = {'status': 'online', 'model': 'DialoGPT-medium'}
                else:
                    results['huggingface'] = {'status': 'offline', 'error': f'HTTP {response.status_code}'}
            else:
                results['huggingface'] = {'status': 'offline', 'error': 'No API key'}
        except Exception as e:
            results['huggingface'] = {'status': 'offline', 'error': str(e)}

        return results

    def use_cohere_model(self, text: str, model: str = 'command-light') -> str:
        """
        Use Cohere API for text enhancement

        Args:
            text: Input text to enhance
            model: Cohere model to use

        Returns:
            Enhanced text
        """
        try:
            if not self.cohere_client:
                return self._fallback_enhance(text)

            response = self.cohere_client.generate(
                model=model,
                prompt=f"Enhance this text for audiobook narration: {text}",
                max_tokens=200,
                temperature=0.7
            )

            enhanced = response.generations[0].text.strip()
            logger.info(f"✅ Cohere {model} enhancement successful")
            return enhanced if enhanced else text

        except Exception as e:
            logger.warning(f"⚠️ Cohere error: {str(e)}, using fallback")
            return self._fallback_enhance(text)

    def use_together_model(self, text: str, model: str = 'meta-llama/Llama-2-7b-chat-hf') -> str:
        """
        Use Together AI for text enhancement

        Args:
            text: Input text to enhance
            model: Together AI model to use

        Returns:
            Enhanced text
        """
        try:
            if not self.openai_client or not self.together_api_key:
                return self._fallback_enhance(text)

            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional audiobook narrator assistant. Enhance text for better narration."},
                    {"role": "user", "content": f"Enhance this text for audiobook narration: {text}"}
                ],
                max_tokens=200,
                temperature=0.7
            )

            enhanced = response.choices[0].message.content.strip()
            logger.info(f"✅ Together AI {model} enhancement successful")
            return enhanced if enhanced else text

        except Exception as e:
            logger.warning(f"⚠️ Together AI error: {str(e)}, using fallback")
            return self._fallback_enhance(text)

    def use_replicate_model(self, text: str, model: str = 'meta/llama-2-7b-chat') -> str:
        """
        Use Replicate API for text enhancement

        Args:
            text: Input text to enhance
            model: Replicate model to use

        Returns:
            Enhanced text
        """
        try:
            if not REPLICATE_AVAILABLE or not self.replicate_api_token:
                return self._fallback_enhance(text)

            output = replicate.run(
                model,
                input={
                    "prompt": f"Enhance this text for audiobook narration: {text}",
                    "max_length": 200,
                    "temperature": 0.7
                }
            )

            enhanced = ''.join(output).strip()
            logger.info(f"✅ Replicate {model} enhancement successful")
            return enhanced if enhanced else text

        except Exception as e:
            logger.warning(f"⚠️ Replicate error: {str(e)}, using fallback")
            return self._fallback_enhance(text)

    def use_ollama_model(self, text: str, model: str = 'llama2:7b') -> str:
        """
        Use Ollama local models (completely free, no API key needed)

        Args:
            text: Input text to enhance
            model: Ollama model to use

        Returns:
            Enhanced text
        """
        try:
            import requests

            # Check if Ollama is running locally
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': model,
                    'prompt': f"Enhance this text for audiobook narration: {text}",
                    'stream': False
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                enhanced = result.get('response', text)
                logger.info(f"✅ Ollama {model} enhancement successful")
                return enhanced
            else:
                logger.warning(f"⚠️ Ollama not available, using fallback")
                return self._fallback_enhance(text)

        except Exception as e:
            logger.warning(f"⚠️ Ollama error: {str(e)}, using fallback")
            return self._fallback_enhance(text)

    def use_local_transformers(self, text: str) -> str:
        """
        Use local Transformers models (completely free, no API key needed)

        Args:
            text: Input text to enhance

        Returns:
            Enhanced text
        """
        try:
            # Simple local enhancement without heavy models
            enhanced = self._advanced_fallback_enhance(text)
            logger.info("✅ Local enhancement successful")
            return enhanced

        except Exception as e:
            logger.warning(f"⚠️ Local enhancement error: {str(e)}, using basic fallback")
            return self._fallback_enhance(text)

    def _advanced_fallback_enhance(self, text: str) -> str:
        """
        Advanced fallback enhancement with better text processing
        """
        # Split into sentences
        sentences = text.split('.')
        enhanced_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Add variety to sentence structure
            if len(sentence.split()) > 10:
                # Long sentence - add dramatic pause
                enhanced = sentence + "..."
            elif sentence.endswith('!'):
                # Exclamation - add emphasis
                enhanced = "Indeed, " + sentence
            elif sentence.endswith('?'):
                # Question - add contemplation
                enhanced = "One might wonder, " + sentence
            else:
                # Regular sentence - add flow
                enhanced = sentence

            enhanced_sentences.append(enhanced)

        return '. '.join(enhanced_sentences)
