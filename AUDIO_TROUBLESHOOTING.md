# 🔧 EchoVerse Audio Generation Troubleshooting Guide

## 🚨 Problem: Audio Shows 0 Seconds Duration

### 📋 Quick Diagnosis Steps

1. **Test IBM Granite Connection First**
   - Click on "AI Models" in the navbar
   - Select "Test Granite Model"
   - This will tell you if the connection is working

2. **Check Current Granite URL**
   - Look at the test results to see the current URL
   - Compare with your Google Colab ngrok URL

### 🔄 Step-by-Step Fix Process

#### Step 1: Restart Google Colab
```
1. Go to your Google Colab notebook
2. Click "Runtime" → "Restart and run all"
3. Wait for all cells to complete
4. Copy the NEW ngrok URL (it changes every restart!)
```

#### Step 2: Update EchoVerse URL
```bash
# Method 1: Use the update script
python update_colab_url.py

# Method 2: Manual update in .env file
# Edit GRANITE_API_URL=https://your-new-ngrok-url.ngrok-free.app
```

#### Step 3: Restart EchoVerse
```bash
# Stop current app (Ctrl+C in terminal)
python app.py
```

#### Step 4: Test the Connection
```
1. Go to http://127.0.0.1:5000
2. Click "AI Models" → "Test Granite Model"
3. Should show "✅ Connection Successful!"
```

#### Step 5: Test Audio Generation
```
1. Go to Create Audiobook page
2. Enter some text (try: "Hello, this is a test of the audio generation system.")
3. Select a tone
4. Click "Create Audiobook with AI"
5. Should show actual processing time, not 0 seconds
```

## 🎯 What to Look For

### ✅ Signs It's Working:
- Test Granite shows "Connection Successful"
- Processing steps show real progress (not instant)
- Audio duration shows actual time (e.g., "15 seconds")
- Download button appears with working MP3 file

### ❌ Signs It's NOT Working:
- Test Granite shows "Connection Failed"
- Processing completes instantly (0-1 seconds)
- Audio duration shows "0 seconds"
- No download button or broken audio file

## 🔍 Common Issues & Solutions

### Issue 1: "Connection Failed" Error
**Cause**: Colab is not running or ngrok URL is wrong
**Solution**: 
1. Check if Colab notebook is running
2. Verify ngrok URL is correct and accessible
3. Make sure Colab didn't go to sleep

### Issue 2: "Connection Successful" but Still 0 Seconds
**Cause**: Granite is connected but TTS or audio processing failed
**Solution**:
1. Check Flask logs for TTS errors
2. Try different text (avoid special characters)
3. Try different tone selection

### Issue 3: Very Long Processing Time
**Cause**: Colab resources are limited or text is too long
**Solution**:
1. Use shorter text (under 500 words)
2. Wait for Colab to allocate more resources
3. Try restarting Colab for fresh resources

## 🛠️ Advanced Debugging

### Check Flask Logs
```bash
# Look for these in the terminal running app.py:
# ✅ "Granite API Client initialized with URL: https://..."
# ✅ "Text enhancement completed successfully"
# ❌ "Connection error" or "Timeout"
```

### Test Granite URL Directly
```bash
# Test if the URL is accessible:
curl -X POST https://your-ngrok-url.ngrok-free.app/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "test", "tone": "neutral"}'
```

### Manual URL Update
```bash
# If the script doesn't work, manually edit .env:
nano .env
# Change: GRANITE_API_URL=https://new-url.ngrok-free.app
```

## 📱 Pro Tips for Reliable Audio Generation

1. **Keep Colab Active**: Don't let it go idle for too long
2. **Use Colab Pro**: For more reliable resources (if available)
3. **Test Connection First**: Always test before creating audiobooks
4. **Short Text First**: Test with short text before long content
5. **Monitor Logs**: Watch Flask terminal for error messages

## 🎉 Expected Working Flow

When everything is working correctly:

```
1. Text Analysis: 2-3 seconds ✅
2. IBM Granite Enhancement: 3-5 seconds ✅
3. Voice Synthesis: 5-10 seconds ✅
4. Audio Processing: 2-3 seconds ✅
5. Total Time: 15-25 seconds ✅
6. Download: Working MP3 file ✅
```

## 🆘 Still Not Working?

If you've tried everything above:

1. **Check Colab Logs**: Look for errors in the Colab notebook
2. **Try Different Text**: Some text might cause issues
3. **Restart Everything**: Colab → Update URL → Restart Flask
4. **Check Internet**: Ensure stable connection to Colab

## 📞 Quick Test Commands

```bash
# 1. Test if app is running
curl http://127.0.0.1:5000/api/health

# 2. Test Granite connection
curl -X POST http://127.0.0.1:5000/api/test-granite

# 3. Update URL quickly
python update_colab_url.py https://your-new-url.ngrok-free.app
```

Remember: **The ngrok URL changes EVERY TIME you restart Google Colab!** 🔄
