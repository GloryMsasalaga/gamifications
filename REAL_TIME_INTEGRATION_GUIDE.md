# 🚀 Real-Time Integration: Africa's Talking + ngrok + Django

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- ✅ Django EduGame project running
- ✅ Africa's Talking account 
- ✅ ngrok installed
- ✅ Phone number for testing

## 🔧 Step 1: Install & Setup ngrok

### Download & Install ngrok
```bash
# Option 1: Download from https://ngrok.com/download
# Option 2: Using chocolatey (Windows)
choco install ngrok

# Option 3: Using npm
npm install -g ngrok
```

### Authenticate ngrok (Optional but Recommended)
1. Sign up at https://dashboard.ngrok.com/signup
2. Get your auth token from dashboard
3. Run: `ngrok authtoken YOUR_AUTH_TOKEN`

## 🌐 Step 2: Start Django Development Server

```bash
# Navigate to your project
cd c:\Users\hp\hackathon\edugame

# Start Django server on port 8000
python manage.py runserver 0.0.0.0:8000
```

**Keep this terminal open!**

## 🔗 Step 3: Create ngrok Tunnel

Open a **NEW terminal** and run:

```bash
# Create public tunnel to your Django server
ngrok http 8000
```

You'll see output like:
```
Session Status                online
Account                       your_email@example.com
Version                       3.0.0
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123def.ngrok.io -> http://localhost:8000
Forwarding                    http://abc123def.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the HTTPS URL** (e.g., `https://abc123def.ngrok.io`) - you'll need this!

**Keep this terminal open too!**

## 📱 Step 4: Configure Africa's Talking

### 4.1 Login to Africa's Talking Dashboard
1. Go to https://account.africastalking.com/
2. Login with your credentials
3. Navigate to **SMS** section

### 4.2 Set Webhook URL
1. Click on **"SMS"** → **"Callback URLs"**
2. Set **Delivery Reports URL**: `https://YOUR_NGROK_URL.ngrok.io/sms/receive/`
3. Set **Incoming Messages URL**: `https://YOUR_NGROK_URL.ngrok.io/sms/receive/`

**Example**: If your ngrok URL is `https://abc123def.ngrok.io`, set:
- `https://abc123def.ngrok.io/sms/receive/`

### 4.3 Configure Sandbox (for Testing)
1. Go to **"Launch Simulator"** or **"Sandbox"**
2. Add your phone number to sandbox
3. Note your **Username** and **API Key**

## 🔑 Step 5: Update Django Settings

Update your `.env` file or settings:

```bash
# In c:\Users\hp\hackathon\edugame\.env
AT_USERNAME=sandbox  # or your live username
AT_API_KEY=your_api_key_here
ADMIN_PHONE_NUMBER=+255628225468
```

## 🧪 Step 6: Test the Integration

### 6.1 Test Webhook Endpoint
Open browser and visit:
```
https://YOUR_NGROK_URL.ngrok.io/sms/receive/
```

You should see an error (since it's expecting POST), but this confirms the URL is accessible.

### 6.2 Test SMS Reception
1. Send SMS to Africa's Talking sandbox number
2. Text: "START" to begin quiz
3. Watch your Django console for incoming requests

### 6.3 Test SMS Sending
Use the start quiz endpoint:
```
https://YOUR_NGROK_URL.ngrok.io/start-quiz/
```

## 📊 Step 7: Monitor Real-Time Activity

### Django Console
Watch for logs like:
```
Incoming SMS from +255628225468: START
SMS sent to +255628225468: Welcome to EduGame! 🎮...
```

### ngrok Web Interface
Visit http://127.0.0.1:4040 to see:
- All HTTP requests
- Request/response details  
- Timing information
- Error details

## 🔧 Step 8: Troubleshooting Commands

Create this helper script for quick testing:

```python
# test_integration.py
import requests
import json

def test_webhook(ngrok_url):
    """Test webhook endpoint"""
    url = f"{ngrok_url}/sms/receive/"
    data = {
        'from': '+255628225468',
        'text': 'START',
        'to': '12345',
        'id': 'test123',
        'date': '2025-09-27 14:30:00'
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_start_quiz(ngrok_url):
    """Test start quiz endpoint"""
    url = f"{ngrok_url}/start-quiz/"
    data = {'phone_number': '+255628225468'}
    
    try:
        response = requests.post(url, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace with your actual ngrok URL
    ngrok_url = "https://abc123def.ngrok.io"
    
    print("Testing webhook...")
    test_webhook(ngrok_url)
    
    print("\nTesting start quiz...")
    test_start_quiz(ngrok_url)
```

## 🎯 Step 9: Live Demo Flow

### For Hackathon Presentation:

1. **Show the Setup**:
   ```bash
   # Terminal 1: Django server
   python manage.py runserver 0.0.0.0:8000
   
   # Terminal 2: ngrok tunnel  
   ngrok http 8000
   ```

2. **Show Africa's Talking Config**:
   - Display webhook URL in dashboard
   - Show sandbox phone number

3. **Live SMS Demo**:
   - Send "START" from your phone
   - Show Django logs receiving webhook
   - Show SMS response on phone
   - Answer questions with A, B, C, D
   - Show real-time leaderboard updates

4. **Show Monitoring**:
   - Display ngrok web interface (http://127.0.0.1:4040)
   - Show real-time request logs

## ⚡ Quick Commands Summary

```bash
# Start everything for demo
cd c:\Users\hp\hackathon\edugame
python manage.py runserver 0.0.0.0:8000  # Terminal 1

ngrok http 8000  # Terminal 2

# Test endpoints
curl -X POST https://YOUR_NGROK_URL.ngrok.io/sms/receive/ \
  -d "from=+255628225468&text=START"

# View leaderboard
https://YOUR_NGROK_URL.ngrok.io/leaderboard/
```

## 🚨 Common Issues & Solutions

### Issue 1: ngrok URL Changes
**Problem**: ngrok URL changes every restart
**Solution**: Use ngrok auth token for persistent URLs, or update Africa's Talking webhook each time

### Issue 2: SMS Not Received
**Problem**: Webhook not being called
**Solution**: 
- Check ngrok tunnel is active
- Verify webhook URL in Africa's Talking dashboard
- Ensure Django server is running on correct port

### Issue 3: CSRF Errors
**Problem**: 403 Forbidden on POST requests
**Solution**: Already handled with `@csrf_exempt` decorator

### Issue 4: SMS Sending Fails
**Problem**: SMS not sent from Django
**Solution**:
- Verify AT_USERNAME and AT_API_KEY
- Check Africa's Talking account balance
- Ensure phone number format (+255...)

## 🎉 You're Ready!

With this setup, you'll have:
- ✅ Real-time SMS receiving via webhooks
- ✅ Automatic SMS responses  
- ✅ Live leaderboard updates
- ✅ Full monitoring and debugging
- ✅ Perfect hackathon demo flow

**Your Tanzania-focused SMS quiz is now live and interactive!** 🇹🇿🎮