from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import africastalking
from .models import User, Question


def index(request):
    """
    Main landing page with game overview and analytics
    """
    # Get some basic stats for the landing page
    total_users = User.objects.count()
    total_questions = Question.objects.count()
    
    # Get top performers for showcase
    top_users = User.objects.order_by('-score')[:3]
    
    context = {
        'total_users': total_users,
        'total_questions': total_questions,
        'top_users': top_users,
    }
    return render(request, 'quiz/index.html', context)


# Initialize Africa's Talking SMS only
def get_sms_service():
    """Initialize SMS service safely"""
    try:
        africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
        return africastalking.SMS
    except Exception as e:
        print(f"Warning: Africa's Talking initialization error: {e}")
        return None


def process_answer(phone_number, message_text):
    """
    Core business logic for processing SMS answers.
    Returns tuple: (user, response_message, is_correct)
    """
    # Get or create user
    user, created = User.objects.get_or_create(
        phone_number=phone_number,
        defaults={'score': 0, 'streak': 0, 'current_question_id': 1}
    )
    
    # Handle special commands
    command = message_text.strip().upper()
    
    if command in ['START', 'QUIZ', 'BEGIN']:
        # Reset user to first question and show welcome
        user.current_question_id = 1
        user.save()
        question = Question.objects.first()
        if question:
            response = f"🎮 Welcome to EduGame Quiz!\n\nQ1: {question.text}"
            if question.options:
                response += f"\n{question.get_options_text()}"
                response += "\n\nReply with A, B, C, or D!"
            return user, response, False
        else:
            return user, "No questions available.", False
    
    elif command in ['CURRENT', 'STATUS', 'SCORE']:
        # Show current question and user stats
        try:
            question = Question.objects.get(id=user.current_question_id)
            response_parts = [
                f"📊 Your Stats:",
                f"Score: {user.score}",
                f"Streak: {user.streak}",
                f"Badges: {user.badges or 'None yet'}"
            ]
            if user.badges:
                response_parts.append(f"Badges: {user.badges}")
            
            response_parts.extend([
                f"\n📝 Current Question:",
                question.text
            ])
            
            if question.options:
                response_parts.append(question.get_options_text())
                response_parts.append("\nReply with A, B, C, or D!")
                
            return user, "\n".join(response_parts), False
        except Question.DoesNotExist:
            return user, "No more questions available. Send START to begin again.", False
    
    # Get current question for this user
    try:
        question = Question.objects.get(id=user.current_question_id)
    except Question.DoesNotExist:
        # If question doesn't exist, start from question 1 or get first available
        question = Question.objects.first()
        if not question:
            return user, "No questions available. Please contact administrator.", False
        user.current_question_id = question.id
    
    # Check if answer is correct (supports both letter choices A,B,C,D and full text)
    user_answer = message_text.strip().upper()
    correct_answer = question.correct_answer.strip().upper()
    
    is_correct = False
    
    # Check if user answered with letter choice (A, B, C, D)
    if user_answer in ['A', 'B', 'C', 'D'] and question.options:
        letter_index = ord(user_answer) - ord('A')  # Convert A=0, B=1, C=2, D=3
        if 0 <= letter_index < len(question.options):
            selected_option = question.options[letter_index].strip().upper()
            is_correct = selected_option == correct_answer
    else:
        # Check if user typed the full answer
        is_correct = user_answer == correct_answer
    
    response_parts = []
    
    if is_correct:
        # Award points
        user.score += 10
        user.streak += 1
        
        response_parts.append("✅ Correct!")
        response_parts.append(f"Score: {user.score} (+10)")
        
        # Check for badges
        new_badges = []
        
        # First Steps badge - first correct answer
        if user.score == 10 and not user.has_badge("First Steps"):
            user.add_badge("🏅", "First Steps")
            new_badges.append("🏅 First Steps")
        
        # Brainiac badge - 3 correct in a row
        if user.streak == 3 and not user.has_badge("Brainiac"):
            user.add_badge("🔥", "Brainiac")
            user.score += 5  # Bonus points
            new_badges.append("🔥 Brainiac (+5 bonus)")
        
        # Quiz Master badge - completed all questions
        total_questions = Question.objects.count()
        if user.current_question_id >= total_questions and not user.has_badge("Quiz Master"):
            user.add_badge("🏆", "Quiz Master")
            new_badges.append("🏆 Quiz Master")
        
        if new_badges:
            response_parts.append(f"New badge(s): {', '.join(new_badges)}")
        
        response_parts.append(f"Streak: {user.streak}")
        
        # Move to next question
        next_question = Question.objects.filter(id__gt=user.current_question_id).first()
        if next_question:
            user.current_question_id = next_question.id
            response_parts.append(f"\nNext: {next_question.text}")
            if next_question.options:
                response_parts.append(next_question.get_options_text())
                response_parts.append("\nReply with A, B, C, or D!")
            else:
                response_parts.append("\nReply with your answer!")
        else:
            response_parts.append("\n🎉 You've completed all questions! Great job!")
    
    else:
        # Wrong answer
        user.streak = 0
        response_parts.append("❌ Wrong answer.")
        response_parts.append(f"Correct answer: {question.correct_answer}")
        response_parts.append(f"Score: {user.score}")
        response_parts.append("Streak reset to 0")
        
        # Show same question again or move to next
        response_parts.append(f"\nTry this: {question.text}")
        if question.options:
            response_parts.append(question.get_options_text())
            response_parts.append("Reply with A, B, C, or D!")
    
    user.save()
    
    return user, "\n".join(response_parts), is_correct


@csrf_exempt
@require_http_methods(["POST"])
def receive_sms(request):
    """
    Webhook endpoint for Africa's Talking SMS
    """
    try:
        # Parse Africa's Talking webhook data
        from_number = request.POST.get('from', '')
        message = request.POST.get('text', '')
        
        if not from_number or not message:
            return JsonResponse({
                'success': False, 
                'message': 'Missing required parameters'
            }, status=400)
        
        # Process the answer
        user, response_message, is_correct = process_answer(from_number, message)
        
        # Send SMS reply via Africa's Talking
        sms_sent = False
        try:
            sms_service = get_sms_service()
            if sms_service:
                sms_response = sms_service.send(response_message, [from_number])
                print(f"SMS sent to {from_number}: {sms_response}")
                sms_sent = True
            else:
                print(f"SMS service not available - response prepared for {from_number}")
        except Exception as sms_error:
            print(f"SMS sending failed: {sms_error}")
            # Continue processing even if SMS fails
        
        return JsonResponse({
            'success': True,
            'user_score': user.score,
            'user_streak': user.streak,
            'is_correct': is_correct,
            'response_sent': sms_sent,
            'response_message': response_message  # Include response for testing
        })
    
    except Exception as e:
        print(f"Error in receive_sms: {e}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def leaderboard(request):
    """
    Display leaderboard with auto-refresh
    """
    users = User.objects.all().order_by('-score', '-updated_at')[:20]
    
    context = {
        'users': users,
        'total_users': User.objects.count(),
    }
    
    return render(request, 'quiz/leaderboard.html', context)


@csrf_exempt
def start_quiz(request):
    """
    Helper endpoint to send first question to a phone number
    """
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                defaults={'current_question_id': 1}
            )
            
            question = Question.objects.first()
            if question:
                message = f"Welcome to EduGame! 🎮\n\n{question.text}"
                if question.options:
                    message += f"\n{question.get_options_text()}"
                    message += "\n\nReply with A, B, C, or D!"
                else:
                    message += "\n\nReply with your answer!"
                
                try:
                    sms_service = get_sms_service()
                    if sms_service:
                        sms_response = sms_service.send(message, [phone_number])
                        return JsonResponse({'success': True, 'message': 'Quiz started!'})
                    else:
                        return JsonResponse({'success': False, 'message': 'SMS service not available'})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
            
            return JsonResponse({'success': False, 'message': 'No questions available'})
    
    return JsonResponse({'success': False, 'message': 'POST method required'})


def my_dashboard(request):
    """
    Personal dashboard showing your quiz progress
    """
    admin_phone = settings.ADMIN_PHONE_NUMBER
    
    # Get your user data
    try:
        user = User.objects.get(phone_number=admin_phone)
    except User.DoesNotExist:
        user = None
    
    # Get current question
    current_question = None
    if user and user.current_question_id:
        try:
            current_question = Question.objects.get(id=user.current_question_id)
        except Question.DoesNotExist:
            current_question = Question.objects.first()
    
    # Get all questions for progress tracking
    all_questions = Question.objects.all().order_by('id')
    total_questions = all_questions.count()
    
    # Calculate progress
    progress_percentage = 0
    if user and total_questions > 0:
        completed = user.current_question_id - 1 if user.current_question_id > 1 else 0
        progress_percentage = (completed / total_questions) * 100
    
    context = {
        'user': user,
        'admin_phone': admin_phone,
        'current_question': current_question,
        'all_questions': all_questions,
        'total_questions': total_questions,
        'progress_percentage': progress_percentage,
        'leaderboard_users': User.objects.all().order_by('-score', '-updated_at')[:5],
    }
    
    return render(request, 'quiz/dashboard.html', context)


@csrf_exempt
def test_sms_offline(request):
    """
    Test SMS functionality without actually sending SMS (for development)
    """
    if request.method == 'POST':
        phone_number = request.POST.get('from', settings.ADMIN_PHONE_NUMBER)
        message = request.POST.get('text', '')
        
        if not message:
            return JsonResponse({
                'success': False, 
                'message': 'Please provide a text message'
            })
        
        # Process the answer using the same logic as SMS webhook
        user, response_message, is_correct = process_answer(phone_number, message)
        
        return JsonResponse({
            'success': True,
            'user_score': user.score,
            'user_streak': user.streak,
            'is_correct': is_correct,
            'response_message': response_message,
            'phone_number': phone_number,
            'test_mode': True
        })
    
    return JsonResponse({'success': False, 'message': 'POST method required'})
