# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### ❌ WhatsApp Sandbox Error
## CSRF Token Issues Fixed ✅

The CSRF (Cross-Site Request Forgery) protection error has been resolved by adding `@csrf_exempt` decorators to the SMS endpoints:

- `/receive_sms/` - Africa's Talking webhook endpoint
- `/start_quiz/` - Quiz initialization endpoint  
- `/test_sms/` - Testing endpoint (no actual SMS)

## Common Issues and Solutions

### Issue 1: Africa's Talking WhatsApp Sandbox Not Available
**Solution**: This app only uses SMS, not WhatsApp. The error can be safely ignored.

**What we've implemented:**
- SMS-only initialization in `views.py`
- Graceful error handling for SMS sending
- Test endpoints that work without SMS service

### 🧪 Testing Without SMS Service

If you don't have Africa's Talking credentials yet, you can still test the game logic:

```powershell
# Test the game logic without sending actual SMS
curl -X POST http://localhost:3000/test_sms/ -d "from=+254700123456&text=NAIROBI"
```

Or use the "🧪 Test Answer (No SMS)" button on the dashboard.

### 📱 SMS Service Setup

1. **Get Africa's Talking Credentials:**
   - Sign up at: https://account.africastalking.com/
   - Get your `AT_USERNAME` and `AT_API_KEY`
   - For testing, use `sandbox` as username

2. **Update .env file:**
   ```
   AT_USERNAME=sandbox
   AT_API_KEY=your_actual_api_key_here
   ADMIN_PHONE_NUMBER=+254700123456
   ```

3. **Test SMS sending:**
   ```powershell
   python manage.py start_my_quiz
   ```

### 🐛 Server Won't Start

**Common causes:**
1. **Import errors**: Check if all dependencies are installed
   ```powershell
   pip install -r requirements.txt
   ```

2. **Database not migrated**:
   ```powershell
   python manage.py migrate
   python manage.py seed_questions
   ```

3. **Port already in use**:
   ```powershell
   # Try a different port
   python manage.py runserver 8000
   ```

### 📊 Dashboard Not Loading

1. **Check URL**: Visit `http://localhost:3000/dashboard/`
2. **Check phone number**: Set `ADMIN_PHONE_NUMBER` in `.env`
3. **Database**: Run `python manage.py seed_questions`

### 🔄 Real SMS Integration

Once you have valid Africa's Talking credentials:

1. **Start ngrok**: `ngrok http 3000`
2. **Set webhook**: Copy ngrok URL to Africa's Talking dashboard
3. **Test real SMS**: Send SMS to your Africa's Talking shortcode

### 🎯 Development Mode Features

- **Test SMS endpoint**: `/test_sms/` - Test without sending actual SMS
- **Dashboard**: Real-time progress tracking
- **Error handling**: Graceful fallbacks when SMS service unavailable

## Quick Commands Reference

```powershell
# Setup with your phone number
python setup_my_phone.py

# Start server
python manage.py runserver 3000

# Test quiz logic
python manage.py start_my_quiz

# Reset database
python manage.py flush
python manage.py migrate  
python manage.py seed_questions

# Test without SMS
curl -X POST http://localhost:3000/test_sms/ -d "from=+254700123456&text=MARS"
```

## Contact Support

If you continue having issues:
1. Check the console output for specific error messages
2. Ensure all environment variables are set correctly
3. Test the web interface first before SMS integration