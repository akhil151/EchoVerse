"""
EchoVerse - Professional AI Audiobook Creation Platform
=======================================================
Flask application with Google Colab IBM Granite + Free LLM APIs
Creates extraordinary audiobooks with innovative AI features.
"""

import os
import logging
import uuid
import json
import requests
import shutil
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our professional services
from services.granite_client import GraniteAPIClient
from services.llm_apis import LLMAPIManager
from services.ai_features import AIFeaturesManager
from audio.professional_tts import ProfessionalTTSEngine
from utils.text_processor import TextProcessor
from utils.file_handler import FileHandler

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app with professional configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'echoverse-professional-2024')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/audio', exist_ok=True)

# Global service instances
granite_client = None
llm_manager = None
ai_features = None
tts_engine = None
text_processor = None
file_handler = None

# Configuration for external services
GRANITE_API_URL = os.environ.get('GRANITE_API_URL', 'http://localhost:5000')  # From Google Colab
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')  # Free Groq API key
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')  # Free HF API key

def initialize_services():
    """Initialize all professional services"""
    global granite_client, llm_manager, ai_features, tts_engine, text_processor, file_handler
    
    try:
        logger.info("🚀 Initializing EchoVerse Professional Services...")
        
        # Initialize IBM Granite client (Google Colab)
        granite_client = GraniteAPIClient(GRANITE_API_URL)
        
        # Initialize free LLM APIs
        llm_manager = LLMAPIManager(
            groq_api_key=GROQ_API_KEY,
            huggingface_api_key=HUGGINGFACE_API_KEY
        )
        
        # Initialize AI features manager
        ai_features = AIFeaturesManager(llm_manager)
        
        # Initialize audio processing
        tts_engine = ProfessionalTTSEngine()
        
        # Initialize utilities
        text_processor = TextProcessor()
        file_handler = FileHandler()
        
        logger.info("✅ All professional services initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {str(e)}")
        return False

# Routes
@app.route('/')
def index():
    """Professional dashboard"""
    return render_template('index.html')



@app.route('/features')
def features():
    """Showcase innovative AI features"""
    return render_template('features.html')

@app.route('/api/health')
def health_check():
    """System health check"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'granite_client': granite_client is not None,
            'llm_manager': llm_manager is not None,
            'ai_features': ai_features is not None,
            'tts_engine': tts_engine is not None
        }
    }
    return jsonify(status)

@app.route('/api/test-granite', methods=['POST'])
def test_granite_connection():
    """Test IBM Granite model connection"""
    try:
        logger.info("🧪 Testing IBM Granite 3.2 connection...")

        # Test with simple text
        test_text = "Hello, this is a test message to verify IBM Granite 3.2 is working properly."

        # Try to transform the text using Granite
        enhanced_text = granite_client.transform_text(
            text=test_text,
            tone='professional'
        )

        if enhanced_text and enhanced_text != test_text:
            logger.info("✅ IBM Granite 3.2 connection successful!")
            return jsonify({
                'status': 'success',
                'message': 'IBM Granite 3.2 is working properly!',
                'original_text': test_text,
                'enhanced_text': enhanced_text,
                'granite_url': os.getenv('GRANITE_API_URL'),
                'timestamp': datetime.now().isoformat()
            })
        else:
            logger.warning("⚠️ IBM Granite 3.2 returned same text - may not be working")
            return jsonify({
                'status': 'warning',
                'message': 'Granite model responded but may not be enhancing text properly',
                'original_text': test_text,
                'enhanced_text': enhanced_text,
                'granite_url': os.getenv('GRANITE_API_URL')
            })

    except Exception as e:
        logger.error(f"❌ IBM Granite 3.2 connection failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to connect to IBM Granite 3.2: {str(e)}',
            'granite_url': os.getenv('GRANITE_API_URL'),
            'suggestion': 'Please check if Google Colab is running and ngrok URL is correct'
        }), 500

@app.route('/api/initialize', methods=['POST'])
def initialize_system():
    """Initialize all AI services"""
    try:
        success = initialize_services()
        
        if success:
            # Test connections
            granite_status = granite_client.test_connection() if granite_client else False
            llm_status = llm_manager.test_connections() if llm_manager else False
            
            return jsonify({
                'status': 'success',
                'message': 'All services initialized successfully!',
                'services': {
                    'granite_api': granite_status,
                    'llm_apis': llm_status,
                    'ai_features': ai_features is not None,
                    'tts_engine': tts_engine is not None
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to initialize some services'
            }), 500
            
    except Exception as e:
        logger.error(f"Error in initialize_system: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_audiobook():
    """Process text into professional audiobook"""
    try:
        logger.info("🚀 PROCESS ENDPOINT CALLED!")
        data = request.get_json()
        text = data.get('text', '').strip()
        logger.info(f"📝 Processing text: {text[:50]}...")
        tone = data.get('tone', 'neutral')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not granite_client or not llm_manager or not ai_features or not tts_engine:
            return jsonify({'error': 'Services not initialized. Please initialize first.'}), 500
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        logger.info(f"🎯 Processing audiobook job {job_id}")
        
        # Step 1: Transform text with IBM Granite (Google Colab)
        logger.info("📝 Step 1: IBM Granite text transformation...")
        transformed_text = granite_client.transform_text(text, tone)
        
        # Step 2: Enhance with free LLM APIs
        logger.info("🚀 Step 2: LLM enhancement...")
        enhanced_text = llm_manager.enhance_content(transformed_text)
        
        # Step 3: Analyze emotions and generate insights
        logger.info("🧠 Step 3: AI analysis...")
        analysis = ai_features.analyze_content(enhanced_text)
        
        # Step 4: Generate professional audio
        logger.info("🎵 Step 4: Professional audio generation...")
        audio_file = tts_engine.generate_audio(
            enhanced_text,
            language=language,
            emotion_data=analysis.get('emotions', {}),
            voice_style=analysis.get('recommended_voice', 'neutral')
        )

        # Fix: Rename audio file to match job_id for download
        if audio_file and os.path.exists(audio_file):
            target_path = f"static/audio/{job_id}.mp3"
            try:
                # Use copy instead of rename to avoid cross-device issues
                import shutil
                shutil.copy2(audio_file, target_path)
                # Remove original file after successful copy
                os.remove(audio_file)
                audio_filename = f"{job_id}.mp3"  # Just the filename for frontend
                logger.info(f"🔄 Audio file copied to: {target_path}")
            except Exception as e:
                logger.error(f"❌ Error copying audio file: {e}")
                # Fallback: use original file path
                audio_filename = os.path.basename(audio_file)
        else:
            logger.error("❌ Audio file generation failed!")
            return jsonify({'error': 'Audio generation failed'}), 500

        logger.info(f"✅ Audiobook job {job_id} completed successfully!")

        return jsonify({
            'job_id': job_id,
            'status': 'completed',
            'audio_file': audio_filename,
            'metadata': {
                'original_text': text,
                'transformed_text': transformed_text,
                'enhanced_text': enhanced_text,
                'analysis': analysis,
                'processing_steps': [
                    'IBM Granite transformation',
                    'LLM enhancement',
                    'AI analysis',
                    'Professional audio generation'
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Error processing audiobook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/status', methods=['GET'])
def get_models_status():
    """Get status of all AI models"""
    try:
        status = {
            'granite': {
                'name': 'IBM Granite 3.2',
                'status': 'checking',
                'description': 'Text tone transformation',
                'capabilities': ['text_transformation', 'tone_adjustment', 'style_enhancement']
            },
            'llama': {
                'name': 'Llama 3.1',
                'status': 'checking',
                'description': 'Content enhancement',
                'capabilities': ['content_enhancement', 'text_improvement', 'creative_writing']
            }
        }

        # Test Granite API
        if granite_client:
            granite_status = granite_client.get_api_status()
            if granite_status.get('status') == 'online':
                status['granite']['status'] = 'online'
            else:
                status['granite']['status'] = 'offline'
        else:
            status['granite']['status'] = 'offline'

        # Test other LLM APIs
        if llm_manager:
            try:
                llm_status = llm_manager.test_apis()
                if llm_status.get('groq', {}).get('status') == 'online':
                    status['llama']['status'] = 'online'
                else:
                    status['llama']['status'] = 'offline'
            except AttributeError:
                # Fallback if test_apis method doesn't exist
                if llm_manager.groq_client:
                    status['llama']['status'] = 'online'
                else:
                    status['llama']['status'] = 'offline'
        else:
            status['llama']['status'] = 'offline'

        return jsonify(status)

    except Exception as e:
        logger.error(f"Error getting models status: {str(e)}")
        return jsonify({'error': str(e)}), 500



@app.route('/api/analyze-content', methods=['POST'])
def analyze_content():
    """Analyze content with AI insights"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not ai_features:
            return jsonify({'error': 'AI features not initialized'}), 500
        
        analysis = ai_features.analyze_content(text)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error analyzing content: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-recommendations', methods=['POST'])
def get_voice_recommendations():
    """Get AI voice recommendations"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        genre = data.get('genre', 'general')
        
        if not ai_features:
            return jsonify({'error': 'AI features not initialized'}), 500
        
        recommendations = ai_features.get_voice_recommendations(content, genre)
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Error getting voice recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process files"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file_handler.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from file
            text = file_handler.extract_text(filepath)
            
            return jsonify({
                'filename': filename,
                'text': text,
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<job_id>')
def download_audio(job_id):
    """Download generated audiobook"""
    try:
        audio_path = f"static/audio/{job_id}.mp3"
        
        if os.path.exists(audio_path):
            return send_file(
                audio_path,
                as_attachment=True,
                download_name=f"echoverse_audiobook_{job_id}.mp3",
                mimetype='audio/mpeg'
            )
        else:
            return jsonify({'error': 'Audio file not found'}), 404
            
    except Exception as e:
        logger.error(f"Error downloading audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    """Extract text from uploaded files"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        logger.info(f"📄 Extracting text from: {file.filename}")

        # Use file handler to extract text
        extracted_text = file_handler.extract_text_from_file(file)

        if not extracted_text or not extracted_text.strip():
            return jsonify({'error': 'No text could be extracted from the file'}), 400

        logger.info(f"✅ Successfully extracted {len(extracted_text)} characters")

        return jsonify({
            'status': 'success',
            'text': extracted_text,
            'filename': file.filename,
            'length': len(extracted_text)
        })

    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-story', methods=['POST'])
def generate_story():
    """Generate AI story for jury demonstration"""
    try:
        data = request.get_json()
        theme = data.get('theme', 'adventure')
        length = data.get('length', 'medium')
        character = data.get('character', 'a mysterious protagonist')

        logger.info(f"🎭 Generating story: theme={theme}, length={length}")

        # Story templates for different themes
        story_templates = {
            'adventure': f"Once upon a time, {character} embarked on an extraordinary journey through uncharted territories. The path ahead was filled with challenges that would test their courage and determination. As they climbed the treacherous mountain peaks, they discovered ancient secrets that had been hidden for centuries. Each step forward revealed new mysteries, and with every obstacle overcome, {character} grew stronger and more determined. The adventure would change them forever, teaching valuable lessons about perseverance, friendship, and the power of believing in oneself.",

            'mystery': f"In the quiet town of Willowbrook, {character} stumbled upon a puzzling case that would change everything. Strange occurrences had been reported throughout the neighborhood - mysterious lights in abandoned buildings, whispered conversations in empty streets, and clues that seemed to appear and disappear like shadows. As {character} delved deeper into the investigation, they uncovered a web of secrets that connected the town's past to its present. The truth, when finally revealed, was more shocking than anyone could have imagined.",

            'romance': f"{character} never believed in love at first sight until that fateful autumn evening. The chance encounter at the old bookstore would spark a romance that transcended time and space. Their hearts beat in perfect harmony as they discovered the magic of true connection. Through seasons of joy and challenges, their love story unfolded like the pages of a beautiful novel, proving that sometimes the most unexpected meetings lead to the most extraordinary love stories.",

            'scifi': f"In the year 2157, {character} was chosen for humanity's most important mission. The discovery of an alien signal had changed everything, and now they must venture into the unknown reaches of space. Advanced technology and alien civilizations awaited their arrival. As they traveled through galaxies far from Earth, {character} encountered wonders beyond imagination and faced challenges that would determine the fate of both human and alien species. The future of interstellar relations rested in their capable hands.",

            'fantasy': f"In the mystical realm of Eldoria, {character} possessed a rare gift that could save or destroy the kingdom. Ancient magic flowed through their veins as they faced dragons, wizards, and enchanted forests. The prophecy spoke of a chosen one who would restore balance to the magical world. With a loyal band of companions and powerful artifacts, {character} embarked on a quest that would test not only their magical abilities but also their wisdom, compassion, and strength of character.",

            'horror': f"{character} should never have entered the abandoned mansion on Elm Street. The creaking floors and whispering shadows held dark secrets that had been buried for decades. As night fell, they realized they were not alone in the house of horrors. Every room revealed new terrors, and every attempt to escape led deeper into the nightmare. The mansion seemed to have a life of its own, feeding on fear and trapping souls within its cursed walls. {character} would need all their courage to survive until dawn."
        }

        # Get base story
        base_story = story_templates.get(theme, story_templates['adventure'])

        # Try to enhance with LLM if available
        try:
            enhanced_story = llm_manager.enhance_content(base_story, 'creative')
            if enhanced_story and len(enhanced_story) > len(base_story) * 0.8:
                story = enhanced_story
            else:
                story = base_story
        except Exception as e:
            logger.warning(f"LLM enhancement failed, using template: {str(e)}")
            story = base_story

        # Adjust length based on request
        if length == 'short':
            story = story[:len(story)//2] + "..."
        elif length == 'long':
            story += f" The adventure continued as {character} discovered even more challenges and wonders, each more incredible than the last. This was only the beginning of an epic tale that would be remembered for generations."

        return jsonify({
            'status': 'success',
            'story': story,
            'theme': theme,
            'length': length,
            'character': character,
            'word_count': len(story.split()),
            'estimated_duration': f"{len(story.split()) // 150 + 1}-{len(story.split()) // 100 + 2} minutes"
        })

    except Exception as e:
        logger.error(f"Story generation error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate story. Please try again.'
        }), 500

@app.route('/create')
def create():
    """Handle pre-filled text from story generator"""
    text = request.args.get('text', '')
    demo = request.args.get('demo', '')

    if demo == 'jury':
        # Pre-fill with jury demonstration text
        text = "Welcome to EchoVerse, the professional AI-powered audiobook creation platform. This demonstration showcases our integration with IBM Granite 3.2 AI model, multiple free LLM APIs, and advanced text-to-speech technology. Our platform transforms any text into high-quality audiobooks with professional narration styles, making content accessible and engaging for all audiences."

    return render_template('create.html', prefilled_text=text)

if __name__ == '__main__':
    logger.info("🎬 Starting EchoVerse Professional Platform...")

    # Initialize services on startup
    initialize_services()

    # Print all routes for debugging
    print("\n🔗 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule.rule}")
    print()

    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
