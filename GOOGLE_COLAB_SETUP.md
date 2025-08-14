# 🚀 Google Colab Setup for IBM Granite Model

## 📋 **Step-by-Step Instructions**

### **Step 1: Open Google Colab**
1. Go to [Google Colab](https://colab.research.google.com/)
2. Sign in with your Google account
3. Click "New Notebook"

### **Step 2: Upload the Notebook**
1. Click "File" → "Upload notebook"
2. Upload the `colab_setup/IBM_Granite_Server.ipynb` file
3. Or copy the notebook content manually

### **Step 3: Set Runtime to GPU**
1. Click "Runtime" → "Change runtime type"
2. Select "GPU" as Hardware accelerator
3. Choose "T4 GPU" (free tier)
4. Click "Save"

### **Step 4: Get Free ngrok Token (Optional but Recommended)**
1. Go to [ngrok.com](https://ngrok.com/)
2. Sign up for free account
3. Go to [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
4. Copy your authtoken
5. In the notebook, replace `YOUR_NGROK_TOKEN_HERE` with your token

### **Step 5: Run the Notebook**
1. Run all cells in order (Ctrl+F9 or Runtime → Run all)
2. Wait for model to download (5-10 minutes first time)
3. Copy the ngrok URL from the output

### **Step 6: Update Your Flask App**
1. Open your `app.py` file
2. Find the line: `GRANITE_API_URL = os.environ.get('GRANITE_API_URL', 'http://localhost:5000')`
3. Replace with your ngrok URL: `GRANITE_API_URL = 'https://your-ngrok-url.ngrok.io'`

---

## 🔧 **Free API Keys Setup**

### **Groq API (Free)**
1. Go to [Groq Console](https://console.groq.com/)
2. Sign up for free account
3. Go to API Keys section
4. Create new API key
5. Add to your environment: `GROQ_API_KEY=your_groq_key_here`

### **Hugging Face API (Free)**
1. Go to [Hugging Face](https://huggingface.co/)
2. Sign up for free account
3. Go to Settings → Access Tokens
4. Create new token with "Read" permissions
5. Add to your environment: `HUGGINGFACE_API_KEY=your_hf_key_here`

---

## 🌐 **Environment Variables Setup**

Create a `.env` file in your project root:

```env
# IBM Granite API (from Google Colab)
GRANITE_API_URL=https://your-ngrok-url.ngrok.io

# Free LLM APIs
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_token_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
```

---

## 🚀 **Running Your Application**

### **Method 1: With Environment Variables**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (Windows)
set GRANITE_API_URL=https://your-ngrok-url.ngrok.io
set GROQ_API_KEY=your_groq_key
set HUGGINGFACE_API_KEY=your_hf_key

# Set environment variables (Linux/Mac)
export GRANITE_API_URL=https://your-ngrok-url.ngrok.io
export GROQ_API_KEY=your_groq_key
export HUGGINGFACE_API_KEY=your_hf_key

# Run the application
python app.py
```

### **Method 2: Direct Code Update**
Update `app.py` directly:
```python
# Replace these lines in app.py
GRANITE_API_URL = 'https://your-ngrok-url.ngrok.io'
GROQ_API_KEY = 'your_groq_api_key_here'
HUGGINGFACE_API_KEY = 'your_huggingface_token_here'
```

---

## 🎯 **Testing the Setup**

### **1. Test IBM Granite Connection**
```bash
curl https://your-ngrok-url.ngrok.io/health
```

### **2. Test Text Transformation**
```bash
curl -X POST https://your-ngrok-url.ngrok.io/transform \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "tone": "dramatic"}'
```

### **3. Test Flask Application**
1. Start your Flask app: `python app.py`
2. Open: `http://localhost:5000`
3. Click "AI Models" → "Initialize System"
4. Check that all services show as "Ready"

---

## 🔍 **Troubleshooting**

### **Common Issues:**

#### **1. ngrok URL Not Working**
- Make sure Google Colab notebook is still running
- ngrok URLs expire when notebook stops
- Get new URL by rerunning the ngrok cell

#### **2. Model Loading Fails**
- Check GPU is enabled in Colab
- Restart runtime if out of memory
- Try using smaller model if needed

#### **3. API Keys Not Working**
- Verify keys are correct and active
- Check API quotas and limits
- Ensure proper permissions

#### **4. Flask App Can't Connect**
- Verify GRANITE_API_URL is correct
- Check firewall/network settings
- Test API endpoint directly

---

## 📊 **Performance Tips**

### **Google Colab Optimization:**
- Use GPU runtime for faster model loading
- Keep notebook active to prevent disconnection
- Monitor RAM usage to avoid crashes

### **API Usage Optimization:**
- Cache responses when possible
- Implement rate limiting
- Use batch processing for multiple requests

### **Flask App Optimization:**
- Enable debug mode for development
- Use production WSGI server for deployment
- Implement proper error handling

---

## 🎉 **Success Checklist**

- [ ] Google Colab notebook running with GPU
- [ ] IBM Granite model loaded successfully
- [ ] ngrok tunnel active and accessible
- [ ] Free API keys obtained and configured
- [ ] Environment variables set correctly
- [ ] Flask application starts without errors
- [ ] System initialization completes successfully
- [ ] All AI models show "Ready" status
- [ ] Text transformation works
- [ ] Audio generation works
- [ ] Innovative features functional

---

## 🚨 **Important Notes**

1. **Keep Colab Running**: Your ngrok URL only works while Colab is active
2. **Free Tier Limits**: Monitor usage to stay within free quotas
3. **Security**: Never commit API keys to version control
4. **Backup**: Save your notebook to Google Drive regularly
5. **Updates**: Check for model updates periodically

---

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all URLs and API keys are correct
3. Test each component individually
4. Check Google Colab and API service status pages

**Your professional AI audiobook platform is ready to impress! 🎧✨**
