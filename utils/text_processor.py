"""
Text Processing Utilities
=========================
Advanced text processing utilities for EchoVerse audiobook creation.
"""

import re
import logging
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

class TextProcessor:
    """
    Advanced Text Processing for EchoVerse
    
    Features:
    - Text cleaning and normalization
    - Sentence and paragraph segmentation
    - Reading time estimation
    - Text complexity analysis
    - Chapter detection
    - Dialogue extraction
    """
    
    def __init__(self):
        """Initialize the text processor"""
        self.download_nltk_data()
        
        # Common abbreviations that shouldn't end sentences
        self.abbreviations = {
            'Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.', 'Sr.', 'Jr.',
            'vs.', 'etc.', 'i.e.', 'e.g.', 'cf.', 'al.', 'Inc.',
            'Ltd.', 'Corp.', 'Co.', 'Ave.', 'St.', 'Rd.', 'Blvd.'
        }
        
        # Dialogue patterns
        self.dialogue_patterns = [
            r'"([^"]*)"',  # Double quotes
            r"'([^']*)'",  # Single quotes
            r'"([^"]*)"',  # Smart quotes
            r"'([^']*)'",  # Smart single quotes (simplified)
        ]
        
        logger.info("Text Processor initialized")
    
    def download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                logger.info("NLTK data downloaded successfully")
            except Exception as e:
                logger.warning(f"Failed to download NLTK data: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text for audiobook processing
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common punctuation issues
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)  # Remove space before punctuation
        text = re.sub(r'([.!?])\s*([a-z])', r'\1 \2', text)  # Ensure space after sentence endings
        
        # Fix quotation marks
        text = re.sub(r'``', '"', text)  # Convert LaTeX quotes
        text = re.sub(r"''", '"', text)
        
        # Normalize dashes
        text = re.sub(r'--+', '—', text)  # Convert multiple dashes to em dash
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)  # Normalize ellipsis
        text = re.sub(r'[!]{2,}', '!', text)    # Remove multiple exclamations
        text = re.sub(r'[?]{2,}', '?', text)    # Remove multiple questions
        
        # Clean up spacing around punctuation
        text = re.sub(r'\s*([—–-])\s*', r' \1 ', text)  # Space around dashes
        
        return text.strip()
    
    def segment_sentences(self, text: str) -> List[str]:
        """
        Segment text into sentences with improved accuracy
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        if not text:
            return []
        
        try:
            # Use NLTK for initial segmentation
            sentences = sent_tokenize(text)
            
            # Post-process to handle abbreviations and edge cases
            corrected_sentences = []
            i = 0
            
            while i < len(sentences):
                sentence = sentences[i]
                
                # Check if sentence ends with abbreviation
                if self._ends_with_abbreviation(sentence) and i + 1 < len(sentences):
                    # Merge with next sentence
                    merged = sentence + ' ' + sentences[i + 1]
                    corrected_sentences.append(merged)
                    i += 2
                else:
                    corrected_sentences.append(sentence)
                    i += 1
            
            return [s.strip() for s in corrected_sentences if s.strip()]
            
        except Exception as e:
            logger.warning(f"Sentence segmentation failed: {str(e)}")
            # Fallback to simple splitting
            return [s.strip() for s in text.split('.') if s.strip()]
    
    def segment_paragraphs(self, text: str) -> List[str]:
        """
        Segment text into paragraphs
        
        Args:
            text: Input text
            
        Returns:
            List of paragraphs
        """
        if not text:
            return []
        
        # Split on double newlines or multiple spaces
        paragraphs = re.split(r'\n\s*\n|\n\s{4,}', text)
        
        # Clean and filter paragraphs
        cleaned_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para and len(para) > 10:  # Filter very short paragraphs
                cleaned_paragraphs.append(para)
        
        return cleaned_paragraphs
    
    def detect_chapters(self, text: str) -> List[Dict]:
        """
        Detect potential chapter breaks in text
        
        Args:
            text: Input text
            
        Returns:
            List of chapter information dictionaries
        """
        chapters = []
        
        # Chapter patterns
        chapter_patterns = [
            r'^(Chapter\s+\d+)',
            r'^(CHAPTER\s+\d+)',
            r'^(\d+\.\s)',
            r'^(Part\s+\d+)',
            r'^(PART\s+\d+)',
            r'^([IVX]+\.\s)',  # Roman numerals
        ]
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            for pattern in chapter_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    chapters.append({
                        'title': match.group(1),
                        'line_number': i,
                        'position': text.find(line),
                        'full_line': line
                    })
                    break
        
        return chapters
    
    def extract_dialogue(self, text: str) -> List[Dict]:
        """
        Extract dialogue from text
        
        Args:
            text: Input text
            
        Returns:
            List of dialogue dictionaries
        """
        dialogues = []
        
        for pattern in self.dialogue_patterns:
            matches = re.finditer(pattern, text)
            
            for match in matches:
                dialogue_text = match.group(1)
                if len(dialogue_text.strip()) > 5:  # Filter very short dialogue
                    dialogues.append({
                        'text': dialogue_text,
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'quote_type': pattern
                    })
        
        # Sort by position
        dialogues.sort(key=lambda x: x['start_pos'])
        
        return dialogues
    
    def analyze_complexity(self, text: str) -> Dict:
        """
        Analyze text complexity for audiobook optimization
        
        Args:
            text: Input text
            
        Returns:
            Complexity analysis dictionary
        """
        if not text:
            return {"error": "No text provided"}
        
        try:
            # Basic metrics
            words = word_tokenize(text.lower())
            sentences = self.segment_sentences(text)
            
            word_count = len(words)
            sentence_count = len(sentences)
            
            # Calculate averages
            avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
            avg_chars_per_word = sum(len(word) for word in words) / word_count if word_count > 0 else 0
            
            # Syllable estimation (simplified)
            syllable_count = self._estimate_syllables(words)
            avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0
            
            # Flesch Reading Ease (simplified)
            if sentence_count > 0 and word_count > 0:
                flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
                flesch_score = max(0, min(100, flesch_score))  # Clamp to 0-100
            else:
                flesch_score = 50
            
            # Determine difficulty level
            if flesch_score >= 70:
                difficulty = "Easy"
            elif flesch_score >= 50:
                difficulty = "Moderate"
            else:
                difficulty = "Difficult"
            
            return {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_words_per_sentence": round(avg_words_per_sentence, 1),
                "avg_chars_per_word": round(avg_chars_per_word, 1),
                "avg_syllables_per_word": round(avg_syllables_per_word, 1),
                "flesch_reading_ease": round(flesch_score, 1),
                "difficulty_level": difficulty,
                "estimated_reading_time_minutes": round(word_count / 200, 1)  # 200 WPM average
            }
            
        except Exception as e:
            logger.error(f"Complexity analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def estimate_audio_duration(self, text: str, words_per_minute: int = 150) -> float:
        """
        Estimate audio duration for text
        
        Args:
            text: Input text
            words_per_minute: Speaking rate (default: 150 WPM)
            
        Returns:
            Estimated duration in minutes
        """
        if not text:
            return 0.0
        
        word_count = len(text.split())
        duration_minutes = word_count / words_per_minute
        
        return round(duration_minutes, 1)
    
    def _ends_with_abbreviation(self, sentence: str) -> bool:
        """Check if sentence ends with a common abbreviation"""
        sentence = sentence.strip()
        
        for abbrev in self.abbreviations:
            if sentence.endswith(abbrev):
                return True
        
        return False
    
    def _estimate_syllables(self, words: List[str]) -> int:
        """
        Estimate syllable count for words (simplified method)
        
        Args:
            words: List of words
            
        Returns:
            Estimated syllable count
        """
        total_syllables = 0
        
        for word in words:
            # Remove punctuation
            word = re.sub(r'[^a-zA-Z]', '', word)
            
            if not word:
                continue
            
            # Simple syllable counting heuristic
            word = word.lower()
            syllables = 0
            
            # Count vowel groups
            vowels = 'aeiouy'
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = is_vowel
            
            # Handle silent e
            if word.endswith('e') and syllables > 1:
                syllables -= 1
            
            # Ensure at least one syllable
            syllables = max(1, syllables)
            
            total_syllables += syllables
        
        return total_syllables
    
    def prepare_for_tts(self, text: str) -> str:
        """
        Prepare text specifically for TTS processing
        
        Args:
            text: Input text
            
        Returns:
            TTS-optimized text
        """
        if not text:
            return ""
        
        # Clean the text
        text = self.clean_text(text)
        
        # Expand common abbreviations for better pronunciation
        abbreviation_expansions = {
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Missus',
            'Ms.': 'Miss',
            'Prof.': 'Professor',
            'vs.': 'versus',
            'etc.': 'etcetera',
            'i.e.': 'that is',
            'e.g.': 'for example',
            'Inc.': 'Incorporated',
            'Ltd.': 'Limited',
            'Corp.': 'Corporation',
            'Co.': 'Company'
        }
        
        for abbrev, expansion in abbreviation_expansions.items():
            text = text.replace(abbrev, expansion)
        
        # Handle numbers (basic)
        text = re.sub(r'\b(\d+)\b', lambda m: self._number_to_words(int(m.group(1))), text)
        
        # Add pauses for better pacing
        text = re.sub(r'([.!?])\s+', r'\1 ', text)  # Ensure space after punctuation
        text = re.sub(r'([,;:])\s*', r'\1 ', text)   # Space after commas, etc.
        
        return text
    
    def _number_to_words(self, num: int) -> str:
        """
        Convert numbers to words (basic implementation)
        
        Args:
            num: Number to convert
            
        Returns:
            Number as words
        """
        if num == 0:
            return "zero"
        
        # Basic number conversion (simplified)
        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", 
                "sixteen", "seventeen", "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        
        if 0 <= num <= 9:
            return ones[num]
        elif 10 <= num <= 19:
            return teens[num - 10]
        elif 20 <= num <= 99:
            return tens[num // 10] + ("" if num % 10 == 0 else " " + ones[num % 10])
        elif 100 <= num <= 999:
            return ones[num // 100] + " hundred" + ("" if num % 100 == 0 else " " + self._number_to_words(num % 100))
        else:
            return str(num)  # Fallback for larger numbers
