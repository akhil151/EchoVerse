# 🎧 EchoVerse - Professional AI Audiobook Creator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![IBM Granite](https://img.shields.io/badge/IBM-Granite%203.2-red.svg)](https://www.ibm.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform text into professional audiobooks with cutting-edge AI technology**

EchoVerse is a world-class audiobook creation platform that combines IBM Granite 3.2 AI with professional TTS engines to create studio-quality audiobooks from any text document.

## ✨ **Key Features**

### 🎨 **World-Class UI/UX**
- **Dynamic Live Wallpaper**: Time-based wallpapers that change throughout the day
- **Innovative Upload System**: Smart drag-and-drop with visual feedback and progress indicators
- **Professional Typography**: Multi-font system with perfect scaling and accessibility
- **Advanced Animations**: Smooth micro-interactions and meaningful transitions
- **Responsive Design**: Flawless experience across all devices and screen sizes

### 🤖 **AI-Powered Intelligence**
- **IBM Granite 3.2**: Advanced text transformation and tone adaptation
- **Multiple LLM Models**: Llama 3.1 and Mistral 7B for content enhancement
- **Smart File Recognition**: Automatic file type detection and processing
- **Emotion Analysis**: AI-driven voice tone recommendations

### 🎵 **Professional Audio**
- **High-Quality TTS**: Multiple voice options with emotion adaptation
- **Audio Effects**: Professional post-processing and enhancement
- **Multiple Formats**: Support for various audio output formats
- **Batch Processing**: Create multiple audiobooks efficiently

### 📁 **File Support**
- **PDF Documents**: Extract and process PDF content
- **Word Documents**: DOCX file support with formatting preservation
- **Text Files**: TXT, MD, RTF format support
- **Smart Processing**: Automatic content optimization

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8 or higher
- Internet connection for AI models
- Google Colab account (for IBM Granite 3.2)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/akhil151/EchoVerse.git
   cd EchoVerse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up IBM Granite 3.2**
   - Open `colab_setup/IBM_Granite_Server.ipynb` in Google Colab
   - Run all cells to start the Granite server
   - Copy the ngrok URL to your `.env` file

5. **Run EchoVerse**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser to: http://127.0.0.1:5000
   - Start creating professional audiobooks!

## 🎯 **How to Use**

### 1. **Upload Your Content**
- Use the innovative drag-and-drop interface
- Support for PDF, DOCX, TXT, MD, and RTF files
- Smart file recognition with visual feedback

### 2. **AI Processing**
- IBM Granite 3.2 analyzes and optimizes your text
- Choose from multiple voice tones and styles
- Real-time processing with progress indicators

### 3. **Generate Audiobook**
- Professional TTS engine creates high-quality audio
- Multiple voice options with emotion adaptation
- Download your completed audiobook

## 🛠 **Technology Stack**

- **Backend**: Flask (Python)
- **AI Models**: IBM Granite 3.2, Llama 3.1, Mistral 7B
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5 with custom enhancements
- **Audio**: Professional TTS engines
- **Deployment**: Docker support included

## 📊 **Project Structure**

```
EchoVerse/
├── 📁 audio/                    # Audio processing modules
├── 📁 services/                 # AI and backend services
├── 📁 static/                   # Web assets (CSS, JS, audio)
├── 📁 templates/                # HTML templates
├── 📁 utils/                    # Utility functions
├── 📁 models/                   # AI model integrations
├── 📁 colab_setup/              # Google Colab setup files
├── 📄 app.py                    # Main Flask application
├── 📄 requirements.txt          # Python dependencies
└── 📄 README.md                 # This file
```

## 🔧 **Configuration**

### Environment Variables
Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# IBM Granite API
GRANITE_API_URL=your-colab-ngrok-url

# Audio Settings
MAX_AUDIO_LENGTH=300
AUDIO_QUALITY=high
```

## 🎨 **UI/UX Features**

- ✅ **Live Wallpaper System** with time-based variations
- ✅ **Innovative Upload Interface** with smart recognition
- ✅ **Professional Typography** with multiple font families
- ✅ **Advanced Animations** and micro-interactions
- ✅ **Comprehensive Accessibility** (WCAG 2.1 AA compliant)
- ✅ **Responsive Design** for all devices
- ✅ **Enhanced Error Handling** with user-friendly feedback
- ✅ **Dark Mode Support** and reduced motion options

## 🧪 **Testing**

Run the comprehensive test suite:

```bash
python test_comprehensive_ui_improvements.py
```

## 📚 **Documentation**

- [Setup Guide](COMPLETE_SETUP_GUIDE.md)
- [Google Colab Setup](GOOGLE_COLAB_SETUP.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [UI/UX Improvements](UI_UX_IMPROVEMENTS_COMPLETE.md)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- IBM for Granite 3.2 AI model
- Google Colab for hosting infrastructure
- Open source community for various libraries and tools

## 📞 **Support**

For support and questions:
- Create an issue on GitHub
- Check the documentation files
- Review the setup guides

---

**🎉 Ready to create professional audiobooks with AI? Get started with EchoVerse today!**