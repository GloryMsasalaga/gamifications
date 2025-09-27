from django.core.management.base import BaseCommand
from django.conf import settings
from quiz.models import Question, User


class Command(BaseCommand):
    help = 'Seeds the database with sample questions and a demo user'
    
    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database with sample data...')
        
        # Clear existing data
        Question.objects.all().delete()
        User.objects.all().delete()
        
        # Sample questions
        questions = [
            {
                'text': 'What programming language is known as the "language of the web"?',
                'correct_answer': 'JAVASCRIPT',
                'options': ['Python', 'JavaScript', 'Java', 'C++'],
                'difficulty_level': 1
            },
            {
                'text': 'What is the capital city of Tanzania?',
                'correct_answer': 'DODOMA',
                'options': ['Dar es Salaam', 'Dodoma', 'Arusha', 'Mwanza'],
                'difficulty_level': 2
            },
            {
                'text': 'What does AI stand for?',
                'correct_answer': 'ARTIFICIAL INTELLIGENCE',
                'options': ['Artificial Intelligence', 'Automated Interface', 'Advanced Integration', 'Applied Innovation'],
                'difficulty_level': 1
            },
            {
                'text': 'Which mountain is the highest peak in Africa?',
                'correct_answer': 'MOUNT KILIMANJARO',
                'options': ['Mount Kenya', 'Mount Kilimanjaro', 'Mount Elgon', 'Mount Meru'],
                'difficulty_level': 1
            },
            {
                'text': 'What does HTTP stand for?',
                'correct_answer': 'HYPERTEXT TRANSFER PROTOCOL',
                'options': ['HyperText Transfer Protocol', 'High Tech Transfer Process', 'HyperText Transmission Protocol', 'Hardware Transfer Text Protocol'],
                'difficulty_level': 2
            },
            {
                'text': 'Which is the largest lake in Africa?',
                'correct_answer': 'LAKE VICTORIA',
                'options': ['Lake Victoria', 'Lake Tanganyika', 'Lake Malawi', 'Lake Chad'],
                'difficulty_level': 1
            },
            {
                'text': 'In which year was Python programming language first released?',
                'correct_answer': '1991',
                'options': ['1989', '1991', '1995', '1998'],
                'difficulty_level': 2
            },
            {
                'text': 'What is the currency of Tanzania?',
                'correct_answer': 'TANZANIAN SHILLING',
                'options': ['Tanzanian Shilling', 'Tanzanian Dollar', 'East African Pound', 'Tanzanian Franc'],
                'difficulty_level': 1
            },
            {
                'text': 'Which company developed the Django web framework?',
                'correct_answer': 'LAWRENCE JOURNAL-WORLD',
                'options': ['Google', 'Facebook', 'Lawrence Journal-World', 'Microsoft'],
                'difficulty_level': 3
            },
            {
                'text': 'What does SMS stand for?',
                'correct_answer': 'SHORT MESSAGE SERVICE',
                'options': ['Simple Message System', 'Short Message Service', 'Swift Messaging Service', 'Secure Message Standard'],
                'difficulty_level': 1
            },
            {
                'text': 'Which African country hosted the 2010 FIFA World Cup?',
                'correct_answer': 'SOUTH AFRICA',
                'options': ['Nigeria', 'South Africa', 'Morocco', 'Egypt'],
                'difficulty_level': 1
            },
            {
                'text': 'Which is the largest city in Tanzania by population?',
                'correct_answer': 'DAR ES SALAAM',
                'options': ['Dodoma', 'Dar es Salaam', 'Mwanza', 'Arusha'],
                'difficulty_level': 1
            },
            {
                'text': 'What is the official language of Tanzania?',
                'correct_answer': 'SWAHILI',
                'options': ['English', 'Swahili', 'Arabic', 'French'],
                'difficulty_level': 1
            },
            {
                'text': 'Which national park in Tanzania is famous for the Great Migration?',
                'correct_answer': 'SERENGETI',
                'options': ['Ngorongoro', 'Serengeti', 'Tarangire', 'Ruaha'],
                'difficulty_level': 2
            }
        ]
        
        # Create questions
        created_count = 0
        for question_data in questions:
            question, created = Question.objects.get_or_create(
                text=question_data['text'],
                defaults=question_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'✅ Created: {question.text[:50]}...')
        
        # Create demo users for testing
        demo_users = [
            {
                'phone_number': settings.ADMIN_PHONE_NUMBER,
                'score': 50,
                'streak': 2,
                'badges': '🏅 First Steps, 🔥 Brainiac',
                'current_question_id': 3
            },
            # You can add more demo users if needed
            # {
            #     'phone_number': '+254700000002', 
            #     'score': 30,
            #     'streak': 1,
            #     'badges': '🏅 First Steps'
            # },
        ]
        
        demo_created = 0
        for user_data in demo_users:
            user, created = User.objects.get_or_create(
                phone_number=user_data['phone_number'],
                defaults=user_data
            )
            if created:
                demo_created += 1
                self.stdout.write(f'👤 Created demo user: {user.phone_number}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'🎉 Successfully seeded database!\n'
                f'   📋 Questions created: {created_count}\n'
                f'   👥 Demo users created: {demo_created}\n'
                f'   🎮 Ready to start the quiz game!'
            )
        )