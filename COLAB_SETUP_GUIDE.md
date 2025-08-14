# 🚀 EchoVerse Google Colab Setup Guide

## ⚠️ IMPORTANT: Audio Generation Fix

The reason your audio generation shows 0 seconds is because the **Google Colab ngrok URL changes every time you restart Colab**. Here's how to fix it:

## 📋 Step-by-Step Fix

### 1. Restart Google Colab
- Go to your Google Colab notebook
- Run all cells to restart the IBM Granite 3.2 server
- Copy the new ngrok URL (it will be different each time)

### 2. Update EchoVerse URL (Choose ONE method)

#### Method A: Using the Update Script (Recommended)
```bash
# In your EchoVerse directory, run:
python update_colab_url.py

# Then enter your new ngrok URL when prompted
# Example: https://abc123-def456.ngrok-free.app
```

#### Method B: Manual Update
1. Open the `.env` file in your EchoVerse directory
2. Find the line: `GRANITE_API_URL=https://old-url.ngrok-free.app`
3. Replace with your new URL: `GRANITE_API_URL=https://new-url.ngrok-free.app`
4. Save the file

### 3. Restart EchoVerse
```bash
# Stop the current Flask app (Ctrl+C)
# Then restart:
python app.py
```

### 4. Test Audio Generation
- Go to http://127.0.0.1:5000/create
- Enter some text
- Select a tone
- Click "Create Audiobook with AI"
- Audio should now generate properly!

## 🔧 Quick Fix Commands

```bash
# 1. Update URL
python update_colab_url.py https://your-new-ngrok-url.ngrok-free.app

# 2. Restart app
python app.py
```

## 🎯 Why This Happens

- **Google Colab** gives you a new ngrok URL every time you restart
- **EchoVerse** needs this URL to connect to IBM Granite 3.2
- **Without the correct URL**, audio generation fails silently

## ✅ Signs It's Working

When properly connected, you should see:
- ✅ Processing steps advance normally
- ✅ Audio duration shows actual time (not 0 seconds)
- ✅ Download button appears with working audio file
- ✅ Console shows successful API calls

## 🚨 Troubleshooting

### Problem: Still getting 0 seconds
**Solution**: Double-check the ngrok URL is correct and Colab is running

### Problem: Connection errors
**Solution**: Make sure Colab notebook is running and ngrok tunnel is active

### Problem: "Model not ready" errors
**Solution**: Wait 1-2 minutes after starting Colab for models to load

## 📱 Pro Tips

1. **Bookmark your Colab notebook** for quick access
2. **Keep Colab tab open** while using EchoVerse
3. **Update URL immediately** after restarting Colab
4. **Test with short text first** to verify connection

## 🎉 Expected Results

Once properly configured:
- **Text Analysis**: ~2-3 seconds
- **AI Enhancement**: ~3-5 seconds  
- **Voice Synthesis**: ~5-10 seconds
- **Audio Processing**: ~2-3 seconds
- **Total Time**: ~15-25 seconds for typical text

Your audio files will be high-quality and properly generated! 🎵
