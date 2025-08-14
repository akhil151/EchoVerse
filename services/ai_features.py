"""
AI Features Manager
==================
Professional manager for innovative AI features using free APIs.
Provides story generation, content analysis, and voice recommendations.
"""

import logging
import random
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import Counter

logger = logging.getLogger(__name__)

class AIFeaturesManager:
    """
    Professional manager for innovative AI features
    
    Features:
    - AI Story Generation
    - Advanced Content Analysis
    - Voice Personality Recommendations
    - Emotion Analysis
    - Genre Detection
    """
    
    def __init__(self, llm_manager):
        """
        Initialize AI Features Manager
        
        Args:
            llm_manager: LLM API Manager instance
        """
        self.llm_manager = llm_manager
        
        # Story generation templates
        self.story_templates = {
            'mystery': {
                'settings': ['old mansion', 'foggy street', 'abandoned library', 'dark alley', 'remote cabin'],
                'characters': ['detective', 'suspect', 'witness', 'victim', 'investigator'],
                'themes': ['murder', 'theft', 'disappearance', 'conspiracy', 'secret'],
                'plot_points': ['discovery of clue', 'false lead', 'revelation', 'confrontation', 'resolution']
            },
            'fantasy': {
                'settings': ['enchanted forest', 'ancient castle', 'magical realm', 'dragon\'s lair', 'wizard tower'],
                'characters': ['wizard', 'knight', 'princess', 'dragon', 'elf', 'dwarf'],
                'themes': ['quest', 'magic', 'prophecy', 'battle', 'treasure'],
                'plot_points': ['call to adventure', 'magical encounter', 'great challenge', 'final battle', 'triumph']
            },
            'sci-fi': {
                'settings': ['space station', 'alien planet', 'futuristic city', 'spaceship', 'laboratory'],
                'characters': ['astronaut', 'scientist', 'alien', 'robot', 'explorer'],
                'themes': ['technology', 'exploration', 'first contact', 'time travel', 'artificial intelligence'],
                'plot_points': ['discovery', 'technological breakthrough', 'alien encounter', 'crisis', 'resolution']
            },
            'romance': {
                'settings': ['charming café', 'beautiful garden', 'seaside town', 'cozy bookstore', 'elegant ballroom'],
                'characters': ['romantic lead', 'love interest', 'best friend', 'rival', 'mentor'],
                'themes': ['first love', 'second chances', 'forbidden love', 'reunion', 'sacrifice'],
                'plot_points': ['first meeting', 'growing attraction', 'conflict', 'separation', 'reunion']
            },
            'adventure': {
                'settings': ['tropical jungle', 'mountain peak', 'desert oasis', 'ancient ruins', 'stormy seas'],
                'characters': ['explorer', 'guide', 'treasure hunter', 'native', 'rival adventurer'],
                'themes': ['treasure hunt', 'survival', 'discovery', 'journey', 'challenge'],
                'plot_points': ['departure', 'first obstacle', 'major discovery', 'final challenge', 'return home']
            }
        }
        
        # Voice personality archetypes
        self.voice_archetypes = {
            'wise_narrator': {
                'description': 'Thoughtful and knowledgeable, perfect for educational content',
                'suitable_genres': ['educational', 'historical', 'philosophical'],
                'characteristics': ['measured pace', 'clear articulation', 'authoritative tone']
            },
            'dramatic_storyteller': {
                'description': 'Passionate and expressive, ideal for emotional narratives',
                'suitable_genres': ['drama', 'romance', 'tragedy'],
                'characteristics': ['dynamic range', 'emotional depth', 'theatrical delivery']
            },
            'mysterious_voice': {
                'description': 'Enigmatic and suspenseful, perfect for thrillers',
                'suitable_genres': ['mystery', 'thriller', 'horror'],
                'characteristics': ['lower register', 'deliberate pacing', 'subtle emphasis']
            },
            'energetic_guide': {
                'description': 'Enthusiastic and engaging, great for adventures',
                'suitable_genres': ['adventure', 'comedy', 'children'],
                'characteristics': ['upbeat tempo', 'varied intonation', 'friendly warmth']
            },
            'gentle_companion': {
                'description': 'Soothing and comforting, ideal for relaxation',
                'suitable_genres': ['meditation', 'self-help', 'bedtime stories'],
                'characteristics': ['soft tone', 'slow pace', 'calming presence']
            },
            'professional_presenter': {
                'description': 'Clear and authoritative, perfect for business content',
                'suitable_genres': ['business', 'technical', 'news'],
                'characteristics': ['crisp diction', 'confident delivery', 'neutral accent']
            }
        }
        
        logger.info("AI Features Manager initialized with story templates and voice archetypes")
    
    def generate_story(self, genre: str = 'mystery', length: str = 'medium') -> Dict[str, Any]:
        """
        Generate AI story using templates and LLM enhancement
        
        Args:
            genre: Story genre
            length: Story length (short, medium, long)
            
        Returns:
            Generated story dictionary
        """
        try:
            logger.info(f"🎭 Generating {genre} story of {length} length")
            
            # Get genre template
            if genre not in self.story_templates:
                genre = 'mystery'  # Default fallback
            
            template = self.story_templates[genre]
            
            # Generate story components
            setting = random.choice(template['settings'])
            main_character = random.choice(template['characters'])
            theme = random.choice(template['themes'])
            plot_points = template['plot_points']
            
            # Create basic story structure
            title = self._generate_title(genre, theme, setting)
            synopsis = self._generate_synopsis(genre, main_character, setting, theme)
            
            # Determine story length
            length_config = {
                'short': {'chapters': 3, 'words_per_chapter': 300},
                'medium': {'chapters': 5, 'words_per_chapter': 500},
                'long': {'chapters': 8, 'words_per_chapter': 700}
            }
            
            config = length_config.get(length, length_config['medium'])
            
            # Generate enhanced story using LLM
            enhanced_synopsis = self.llm_manager.enhance_content(synopsis, 'creative')
            
            story = {
                'title': title,
                'genre': genre.title(),
                'synopsis': enhanced_synopsis,
                'setting': setting,
                'main_character': main_character,
                'theme': theme,
                'plot_points': plot_points,
                'estimated_chapters': config['chapters'],
                'estimated_words': config['chapters'] * config['words_per_chapter'],
                'estimated_audio_minutes': (config['chapters'] * config['words_per_chapter']) // 150,
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Generated story: '{title}'")
            return story
            
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return self._get_default_story()
    
    def analyze_content(self, text: str) -> Dict[str, Any]:
        """
        Analyze content with AI insights
        
        Args:
            text: Text to analyze
            
        Returns:
            Comprehensive content analysis
        """
        try:
            logger.info("🧠 Analyzing content with AI insights")
            
            # Basic text statistics
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            # Genre detection
            detected_genre = self._detect_genre(text)
            
            # Emotion analysis using LLM
            sentiment_data = self.llm_manager.analyze_sentiment(text)
            
            # Complexity assessment
            complexity = self._assess_complexity(text)
            
            # Extract key themes
            themes = self._extract_themes(text)
            
            # Voice recommendations
            voice_recommendations = self._get_voice_recommendations_for_content(text, detected_genre)
            
            analysis = {
                'word_count': len(words),
                'sentence_count': len([s for s in sentences if s.strip()]),
                'paragraph_count': len(paragraphs),
                'avg_sentence_length': len(words) / max(len(sentences), 1),
                
                'detected_genre': detected_genre,
                'complexity': complexity,
                'reading_level': self._estimate_reading_level(complexity),
                
                'sentiment': sentiment_data['sentiment'],
                'sentiment_confidence': sentiment_data['confidence'],
                'emotions': {
                    'primary': sentiment_data['sentiment'],
                    'intensity': sentiment_data['confidence']
                },
                
                'themes': themes,
                'recommended_voice': voice_recommendations[0]['archetype'] if voice_recommendations else 'wise_narrator',
                'voice_options': voice_recommendations,
                
                'estimated_audio_duration': len(words) / 150,  # 150 WPM
                'recommended_pace': self._recommend_pace(complexity, sentiment_data['sentiment']),
                
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Content analysis complete: {detected_genre} genre, {complexity} complexity")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return self._get_default_analysis()
    
    def get_voice_recommendations(self, content: str = '', genre: str = 'general') -> List[Dict[str, Any]]:
        """
        Get voice personality recommendations
        
        Args:
            content: Content to analyze (optional)
            genre: Content genre
            
        Returns:
            List of voice recommendations
        """
        try:
            logger.info(f"🎤 Getting voice recommendations for {genre} genre")
            
            recommendations = []
            
            # Score each archetype
            for archetype_name, archetype in self.voice_archetypes.items():
                score = 0
                
                # Genre matching
                if genre in archetype['suitable_genres']:
                    score += 3
                elif 'general' in archetype['suitable_genres'] or len(archetype['suitable_genres']) > 3:
                    score += 1
                
                # Content analysis (if provided)
                if content:
                    content_lower = content.lower()
                    
                    # Check for genre-specific keywords
                    if genre == 'mystery' and any(word in content_lower for word in ['mystery', 'detective', 'clue', 'suspect']):
                        if archetype_name == 'mysterious_voice':
                            score += 2
                    elif genre == 'adventure' and any(word in content_lower for word in ['adventure', 'journey', 'explore']):
                        if archetype_name == 'energetic_guide':
                            score += 2
                    elif genre == 'drama' and any(word in content_lower for word in ['emotion', 'heart', 'passion']):
                        if archetype_name == 'dramatic_storyteller':
                            score += 2
                
                recommendations.append({
                    'archetype': archetype_name,
                    'description': archetype['description'],
                    'score': score,
                    'characteristics': archetype['characteristics'],
                    'suitable_genres': archetype['suitable_genres']
                })
            
            # Sort by score
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            logger.info(f"✅ Generated {len(recommendations)} voice recommendations")
            return recommendations[:3]  # Return top 3
            
        except Exception as e:
            logger.error(f"Error getting voice recommendations: {str(e)}")
            return [{'archetype': 'wise_narrator', 'description': 'Default narrator', 'score': 1}]
    
    def _generate_title(self, genre: str, theme: str, setting: str) -> str:
        """Generate story title"""
        title_templates = [
            f"The {theme.title()} at {setting.title()}",
            f"Mystery of the {setting.title()}",
            f"The {setting.title()} {theme.title()}",
            f"Secrets of {setting.title()}",
            f"The Last {theme.title()}"
        ]
        return random.choice(title_templates)
    
    def _generate_synopsis(self, genre: str, character: str, setting: str, theme: str) -> str:
        """Generate story synopsis"""
        synopsis_templates = [
            f"A gripping {genre} tale unfolds when a {character} discovers a {theme} in {setting}. What starts as a simple investigation becomes a journey that will change everything.",
            f"In the heart of {setting}, a {character} stumbles upon a {theme} that threatens to unravel their world. Time is running out, and only they can uncover the truth.",
            f"When {setting} becomes the center of an incredible {theme}, a brave {character} must face their greatest fears to solve the mystery that lies hidden beneath the surface."
        ]
        return random.choice(synopsis_templates)
    
    def _detect_genre(self, text: str) -> str:
        """Detect genre from text content"""
        text_lower = text.lower()
        
        genre_keywords = {
            'mystery': ['detective', 'crime', 'murder', 'clue', 'suspect', 'investigation'],
            'fantasy': ['magic', 'wizard', 'dragon', 'spell', 'enchanted', 'quest'],
            'sci-fi': ['space', 'alien', 'robot', 'future', 'technology', 'planet'],
            'romance': ['love', 'heart', 'kiss', 'romance', 'relationship', 'passion'],
            'adventure': ['journey', 'treasure', 'explore', 'adventure', 'quest', 'expedition'],
            'horror': ['fear', 'terror', 'ghost', 'haunted', 'nightmare', 'evil'],
            'drama': ['emotion', 'conflict', 'family', 'relationship', 'struggle']
        }
        
        genre_scores = {}
        for genre, keywords in genre_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                genre_scores[genre] = score
        
        if genre_scores:
            return max(genre_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'general'
    
    def _assess_complexity(self, text: str) -> str:
        """Assess text complexity"""
        words = text.split()
        if not words:
            return 'simple'
        
        avg_word_length = sum(len(word) for word in words) / len(words)
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        if avg_word_length > 6 and avg_sentence_length > 20:
            return 'complex'
        elif avg_word_length > 4 and avg_sentence_length > 15:
            return 'moderate'
        else:
            return 'simple'
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract key themes from text"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        stop_words = {'that', 'this', 'with', 'have', 'will', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other'}
        meaningful_words = [word for word in words if word not in stop_words]
        
        word_counts = Counter(meaningful_words)
        themes = [word for word, count in word_counts.most_common(5) if count >= 2]
        
        return themes[:3]  # Return top 3 themes
    
    def _get_voice_recommendations_for_content(self, text: str, genre: str) -> List[Dict[str, Any]]:
        """Get voice recommendations based on content analysis"""
        return self.get_voice_recommendations(text, genre)
    
    def _estimate_reading_level(self, complexity: str) -> str:
        """Estimate reading level"""
        mapping = {
            'simple': 'Elementary',
            'moderate': 'Middle School',
            'complex': 'High School+'
        }
        return mapping.get(complexity, 'Middle School')
    
    def _recommend_pace(self, complexity: str, sentiment: str) -> str:
        """Recommend narration pace"""
        if complexity == 'complex':
            return 'slow'
        elif sentiment in ['positive', 'excitement']:
            return 'fast'
        else:
            return 'normal'
    
    def _get_default_story(self) -> Dict[str, Any]:
        """Get default story as fallback"""
        return {
            'title': 'The Mysterious Adventure',
            'genre': 'Mystery',
            'synopsis': 'A thrilling tale of discovery and adventure awaits.',
            'setting': 'mysterious location',
            'main_character': 'brave explorer',
            'theme': 'discovery',
            'estimated_chapters': 5,
            'estimated_words': 2500,
            'estimated_audio_minutes': 17,
            'created_at': datetime.now().isoformat()
        }
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis as fallback"""
        return {
            'word_count': 0,
            'sentence_count': 0,
            'paragraph_count': 0,
            'detected_genre': 'general',
            'complexity': 'moderate',
            'sentiment': 'neutral',
            'themes': [],
            'recommended_voice': 'wise_narrator',
            'estimated_audio_duration': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
