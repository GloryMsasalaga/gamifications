# 🎮 EduGame SMS - Django Hackathon MVP

A real-time SMS-based quiz game built with Django and Africa's Talking that updates a leaderboard in real-time. Players answer questions via SMS and earn points, streaks, and badges!

## 🚀 Features

- **Two-way SMS Integration** via Africa's Talking API
- **Real-time Leaderboard** with auto-refresh every 7 seconds
- **Badge System**: 🏅 First Steps, 🔥 Brainiac, 🏆 Quiz Master
- **Scoring System**: +10 points per correct answer, +5 bonus for 3-streak
- **Responsive Web Interface** with beautiful gradients and animations
- **SQLite Database** (no extra setup required)

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- Africa's Talking account (free sandbox available)
- ngrok (for local webhook testing)

## 🏗️ Project Structure

```
edugame/
├── edugame/                 # Django project settings
│   ├── settings.py         # Main configuration
│   └── urls.py             # URL routing
├── quiz/                   # Main app
│   ├── models.py           # User & Question models
│   ├── views.py            # SMS webhook & leaderboard logic
│   ├── urls.py             # App URLs
│   ├── templates/quiz/     # HTML templates
│   ├── management/commands/ # Custom commands
│   └── fixtures/           # Sample data
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🛠️ Installation & Setup

### 1. Clone and Setup Environment

```powershell
# Navigate to your project directory
cd C:\Users\hp\hackathon\edugame

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```powershell
# Copy environment template
copy .env.example .env

# Edit .env file with your Africa's Talking credentials
# You can get these from https://account.africastalking.com/
```

Edit the `.env` file:
```
AT_USERNAME=your_africastalking_username
AT_API_KEY=your_africastalking_api_key
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. Setup Database

```powershell
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed with sample questions and demo users
python manage.py seed_questions

# OR load from fixture
python manage.py loaddata sample_questions.json
```

### 4. Start Development Server

```powershell
# Run Django server
python manage.py runserver 3000
```

## 🌐 Ngrok Setup for SMS Webhooks

### 1. Install and Setup Ngrok

```powershell
# Download ngrok from https://ngrok.com/
# After installation:
ngrok http 3000
```

### 2. Configure Africa's Talking Webhook

1. Copy the HTTPS URL from ngrok (e.g., `https://abc123.ngrok.io`)
2. Go to [Africa's Talking Dashboard](https://account.africastalking.com/)
3. Navigate to SMS → Settings → Callback URL
4. Set webhook URL to: `https://abc123.ngrok.io/receive_sms/`
5. Save settings

## 📱 Testing the SMS Integration

### Option 1: Using Africa's Talking Sandbox

1. Log into your Africa's Talking sandbox
2. Send SMS from sandbox to your webhook
3. Monitor Django console for webhook calls

### Option 2: Using cURL (Simulate Webhook)

```powershell
# Test the webhook endpoint directly
curl -X POST http://localhost:3000/receive_sms/ -d "from=%2B254700123456&text=NAIROBI"
```

### Option 3: Start Quiz via Web Interface

```powershell
# Send initial question to a phone number
curl -X POST http://localhost:3000/start_quiz/ -d "phone_number=+254700123456"
```

## 🎯 How to Play

1. **Send any SMS** to the configured shortcode/number
2. **Receive first question** automatically  
3. **Reply with your answer** (case-insensitive)
4. **Get instant feedback** with score updates
5. **Earn badges** for achievements:
   - 🏅 **First Steps**: Answer your first question correctly
   - 🔥 **Brainiac**: Get 3 correct answers in a row (+5 bonus points)
   - 🏆 **Quiz Master**: Complete all available questions

## 📊 Accessing the Leaderboard

Visit: `http://localhost:3000/leaderboard/`

Features:
- **Auto-refresh** every 7 seconds
- **Real-time rankings** by score
- **Visual badges** and streak indicators  
- **Mobile responsive** design
- **Beautiful animations** and gradients

## 🧪 Sample Questions

The app comes with 6 sample questions:

1. What is the capital of Kenya? (Answer: NAIROBI)
2. Which planet is known as the Red Planet? (Answer: MARS)
3. What is 15 + 27? (Answer: 42)
4. Who wrote "Things Fall Apart"? (Answer: CHINUA ACHEBE)
5. What is the largest mammal? (Answer: BLUE WHALE)
6. Kenya independence year? (Answer: 1963)

## 🔧 API Endpoints

### SMS Webhook
- **URL**: `POST /receive_sms/`
- **Purpose**: Receives Africa's Talking webhooks
- **Parameters**: 
  - `from`: Sender phone number
  - `text`: SMS message content

### Leaderboard
- **URL**: `GET /leaderboard/`
- **Purpose**: Display real-time leaderboard
- **Features**: Auto-refresh, responsive design

### Start Quiz
- **URL**: `POST /start_quiz/`
- **Purpose**: Send first question to a phone number
- **Parameters**:
  - `phone_number`: Target phone number

## 🏆 Scoring System

- **Correct Answer**: +10 points
- **3-Question Streak**: +5 bonus points + 🔥 Brainiac badge
- **Wrong Answer**: Streak resets to 0
- **First Correct**: 🏅 First Steps badge
- **Complete Quiz**: 🏆 Quiz Master badge

## 🐛 Troubleshooting

### SMS Not Received?
1. Check ngrok is running and webhook URL is correct
2. Verify Africa's Talking credentials in `.env`
3. Check Django console for error messages
4. Ensure phone number format includes country code

### Leaderboard Not Updating?
1. Check if auto-refresh is working (7-second countdown)
2. Verify users are being created in database
3. Check Django server logs for errors

### Database Issues?
```powershell
# Reset database
python manage.py flush
python manage.py migrate
python manage.py seed_questions
```

## 📝 Demo Script

Here's a complete demo walkthrough:

```powershell
# 1. Setup (run once)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_questions

# 2. Start servers
# Terminal 1:
python manage.py runserver 3000

# Terminal 2:
ngrok http 3000

# 3. Test webhook manually
curl -X POST http://localhost:3000/receive_sms/ -d "from=%2B254700123456&text=NAIROBI"

# 4. View leaderboard
# Open: http://localhost:3000/leaderboard/

# 5. Start quiz for a phone number
curl -X POST http://localhost:3000/start_quiz/ -d "phone_number=+254700123456"
```

## 🚀 Production Deployment

For production deployment:

1. **Update settings**:
   - Set `DEBUG=False`
   - Add your domain to `ALLOWED_HOSTS`
   - Use PostgreSQL instead of SQLite

2. **Environment variables**:
   - Use production Africa's Talking credentials
   - Generate new SECRET_KEY

3. **Static files**:
   ```python
   python manage.py collectstatic
   ```

4. **Database**:
   ```python
   python manage.py migrate
   python manage.py seed_questions
   ```

## 🛡️ Security Notes

- All sensitive credentials are stored in environment variables
- CSRF exempt only for SMS webhook (required for Africa's Talking)
- Input validation on all user inputs
- SQL injection protection via Django ORM

## 📄 License

This project is open source and available under the MIT License.

---

## 🎮 Ready to Play!

Your EduGame SMS is now ready! Players can start texting to join the quiz, and you can watch the leaderboard update in real-time. 

**Happy coding! 🚀**