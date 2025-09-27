from django.core.management.base import BaseCommand
from django.conf import settings
from quiz.models import Question, User
import africastalking

class Command(BaseCommand):
    help = 'Start a quiz for your phone number'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to start quiz for (defaults to ADMIN_PHONE_NUMBER from settings)',
        )
    
    def handle(self, *args, **options):
        phone_number = options['phone'] or settings.ADMIN_PHONE_NUMBER
        
        if not phone_number or phone_number == '+254700000000':
            self.stdout.write(
                self.style.ERROR(
                    '❌ Please set your ADMIN_PHONE_NUMBER in .env file or use --phone argument\n'
                    'Example: python manage.py start_my_quiz --phone +254700123456'
                )
            )
            return
        
        self.stdout.write(f'🎮 Starting quiz for {phone_number}...')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'current_question_id': 1, 'score': 0, 'streak': 0}
        )
        
        if created:
            self.stdout.write(f'👤 Created new user: {phone_number}')
        else:
            self.stdout.write(f'👤 Found existing user: {phone_number} (Score: {user.score})')
        
        # Get first question
        question = Question.objects.first()
        if not question:
            self.stdout.write(
                self.style.ERROR('❌ No questions found! Run: python manage.py seed_questions')
            )
            return
        
        # Prepare welcome message
        message = f"🎮 Welcome to EduGame SMS!\n\n"
        message += f"Question {user.current_question_id}: {question.text}\n"
        
        if question.options:
            message += f"{question.get_options_text()}\n"
        
        message += f"\n💡 Reply with your answer!"
        message += f"\n📊 Current Score: {user.score}"
        if user.badges:
            message += f"\n🏅 Badges: {user.badges}"
        
        # Try to send SMS
        try:
            # Initialize Africa's Talking SMS only (avoid WhatsApp sandbox issues)
            africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
            sms_service = africastalking.SMS
            
            response = sms_service.send(message, [phone_number])
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Quiz started successfully!\n'
                    f'   📱 SMS sent to: {phone_number}\n'
                    f'   📋 Current question: {question.text}\n'
                    f'   ✅ Response: {response}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Quiz initialized but SMS sending failed: {e}\n'
                    f'   📱 Target phone: {phone_number}\n'
                    f'   💡 Check your AT_USERNAME and AT_API_KEY in .env\n'
                    f'   🔧 You can still test via webhook: /receive_sms/\n'
                    f'   📋 Current question: {question.text}'
                )
            )
        
        self.stdout.write(
            f'\n🌐 You can also view the leaderboard at: http://localhost:3000/leaderboard/'
        )