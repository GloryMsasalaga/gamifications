#!/usr/bin/env python3
"""
Quick setup script for EduGame SMS with your real phone number
"""

import os
import sys

def main():
    print("🎮 EduGame SMS - Quick Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: Please run this script from the edugame directory")
        print("   Example: cd edugame && python setup_my_phone.py")
        sys.exit(1)
    
    # Get phone number
    phone = input("\n📱 Enter your phone number (with country code, e.g., +254700123456): ").strip()
    
    if not phone.startswith('+'):
        print("⚠️  Warning: Phone number should start with + (country code)")
        phone = '+' + phone
    
    # Create or update .env file
    env_content = f"""# Africa's Talking API Configuration
AT_USERNAME=sandbox
AT_API_KEY=your_api_key_here

# Django Configuration  
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True

# Your Configuration
ADMIN_PHONE_NUMBER={phone}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created .env file with your phone number: {phone}")
    
    # Run migrations
    print("\n🔄 Setting up database...")
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    
    # Seed questions
    print("\n🌱 Adding sample questions...")
    os.system('python manage.py seed_questions')
    
    print(f"""
✅ Setup Complete! 

🎯 Quick Actions:
   1. Start quiz for your number: python manage.py start_my_quiz
   2. View your dashboard: http://localhost:3000/dashboard/
   3. Start server: python manage.py runserver 3000

📱 Your phone number: {phone}

🔧 Next Steps:
   1. Get Africa's Talking credentials from: https://account.africastalking.com/
   2. Update AT_USERNAME and AT_API_KEY in .env file
   3. Setup ngrok for webhook testing: ngrok http 3000

Happy gaming! 🚀
""")

if __name__ == '__main__':
    main()