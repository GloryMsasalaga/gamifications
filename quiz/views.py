from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import africastalking
from .models import User, Question


# Initialize Africa's Talking
africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
sms = africastalking.SMS


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
    
    # Get current question for this user
    try:
        question = Question.objects.get(id=user.current_question_id)
    except Question.DoesNotExist:
        # If question doesn't exist, start from question 1 or get first available
        question = Question.objects.first()
        if not question:
            return user, "No questions available. Please contact administrator.", False
        user.current_question_id = question.id
    
    # Check if answer is correct (case-insensitive)
    user_answer = message_text.strip().upper()
    correct_answer = question.correct_answer.strip().upper()
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
        try:
            sms_response = sms.send(response_message, [from_number])
            print(f"SMS sent to {from_number}: {sms_response}")
        except Exception as sms_error:
            print(f"SMS sending failed: {sms_error}")
            # Continue processing even if SMS fails
        
        return JsonResponse({
            'success': True,
            'user_score': user.score,
            'user_streak': user.streak,
            'is_correct': is_correct,
            'response_sent': True
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
                message += "\n\nReply with your answer!"
                
                try:
                    sms_response = sms.send(message, [phone_number])
                    return JsonResponse({'success': True, 'message': 'Quiz started!'})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
            
            return JsonResponse({'success': False, 'message': 'No questions available'})
    
    return JsonResponse({'success': False, 'message': 'POST method required'})
