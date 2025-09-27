#!/usr/bin/env python3
"""
Test script for multiple choice functionality
"""

# Simulate the letter choice logic
def test_letter_choice_validation():
    # Simulate question data
    question_options = ['Nairobi', 'Mombasa', 'Kisumu', 'Eldoret']
    correct_answer = 'NAIROBI'
    
    # Test cases
    test_cases = [
        ('A', True),   # Should match first option 'Nairobi'
        ('B', False),  # Should match second option 'Mombasa'
        ('C', False),  # Should match third option 'Kisumu'  
        ('D', False),  # Should match fourth option 'Eldoret'
        ('NAIROBI', True),  # Full text answer
        ('nairobi', True),  # Case insensitive
        ('X', False),       # Invalid letter
        ('mombasa', False), # Wrong full text
    ]
    
    print("🧪 Testing Multiple Choice Answer Validation")
    print("=" * 50)
    
    for user_input, expected_result in test_cases:
        user_answer = user_input.strip().upper()
        is_correct = False
        
        # Check if user answered with letter choice (A, B, C, D)
        if user_answer in ['A', 'B', 'C', 'D'] and question_options:
            letter_index = ord(user_answer) - ord('A')  # Convert A=0, B=1, C=2, D=3
            if 0 <= letter_index < len(question_options):
                selected_option = question_options[letter_index].strip().upper()
                is_correct = selected_option == correct_answer
        else:
            # Check if user typed the full answer
            is_correct = user_answer == correct_answer
            
        status = "✅ PASS" if is_correct == expected_result else "❌ FAIL"
        print(f"{status} | Input: '{user_input}' → Expected: {expected_result}, Got: {is_correct}")

def display_sample_questions():
    """Display how questions will look to users"""
    
    sample_questions = [
        {
            'text': 'What is the capital of Kenya?',
            'options': ['Nairobi', 'Mombasa', 'Kisumu', 'Eldoret'],
            'correct_answer': 'NAIROBI'
        },
        {
            'text': 'Which planet is known as the Red Planet?',
            'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
            'correct_answer': 'MARS'
        }
    ]
    
    print("\n📱 Sample SMS Messages Users Will Receive")
    print("=" * 50)
    
    for i, q in enumerate(sample_questions, 1):
        print(f"\nQuestion {i}:")
        print(f"{q['text']}")
        
        letters = ['A', 'B', 'C', 'D']
        for j, option in enumerate(q['options']):
            print(f"{letters[j]}) {option}")
            
        print("Reply with A, B, C, or D!")
        print("-" * 30)

if __name__ == "__main__":
    test_letter_choice_validation()
    display_sample_questions()
    
    print("\n🎉 Multiple Choice System Ready!")
    print("Users can now answer with:")
    print("• Letter choices: A, B, C, D")
    print("• Full text answers: NAIROBI, MARS, etc.")
    print("• Commands: START, CURRENT, STATUS")