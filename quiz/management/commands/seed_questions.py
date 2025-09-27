from django.core.management.base import BaseCommand
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
                'text': 'What is the capital of Kenya?',
                'correct_answer': 'NAIROBI',
                'options': ['Nairobi', 'Mombasa', 'Kisumu', 'Eldoret'],
                'difficulty_level': 1
            },
            {
                'text': 'Which planet is known as the Red Planet?',
                'correct_answer': 'MARS',
                'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                'difficulty_level': 1
            },
            {
                'text': 'What is 15 + 27?',
                'correct_answer': '42',
                'options': ['40', '41', '42', '43'],
                'difficulty_level': 1
            },
            {
                'text': 'Who wrote the book "Things Fall Apart"?',
                'correct_answer': 'CHINUA ACHEBE',
                'options': ['Chinua Achebe', 'Wole Soyinka', 'Ngugi wa Thiongo', 'Chimamanda Adichie'],
                'difficulty_level': 2
            },
            {
                'text': 'What is the largest mammal in the world?',
                'correct_answer': 'BLUE WHALE',
                'options': ['Elephant', 'Blue Whale', 'Giraffe', 'Rhinoceros'],
                'difficulty_level': 1
            },
            {
                'text': 'In which year did Kenya gain independence?',
                'correct_answer': '1963',
                'options': ['1960', '1963', '1965', '1970'],
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
                'phone_number': '+254700000001',
                'score': 50,
                'streak': 2,
                'badges': '🏅 First Steps, 🔥 Brainiac'
            },
            {
                'phone_number': '+254700000002', 
                'score': 30,
                'streak': 1,
                'badges': '🏅 First Steps'
            },
            {
                'phone_number': '+254700000003',
                'score': 70,
                'streak': 0,
                'badges': '🏅 First Steps, 🔥 Brainiac, 🏆 Quiz Master'
            }
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