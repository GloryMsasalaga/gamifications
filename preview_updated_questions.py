#!/usr/bin/env python3
"""
Display updated sample questions for EduGame SMS Quiz
"""

def display_updated_questions():
    """Display all the updated sample questions"""
    
    questions = [
        {
            'text': 'What programming language is known as the "language of the web"?',
            'correct_answer': 'JAVASCRIPT',
            'options': ['Python', 'JavaScript', 'Java', 'C++'],
            'difficulty_level': 1,
            'category': 'Technology'
        },
        {
            'text': 'Which African country is known as the "Pearl of Africa"?',
            'correct_answer': 'UGANDA',
            'options': ['Kenya', 'Uganda', 'Tanzania', 'Rwanda'],
            'difficulty_level': 2,
            'category': 'Geography'
        },
        {
            'text': 'What does AI stand for?',
            'correct_answer': 'ARTIFICIAL INTELLIGENCE',
            'options': ['Artificial Intelligence', 'Automated Interface', 'Advanced Integration', 'Applied Innovation'],
            'difficulty_level': 1,
            'category': 'Technology'
        },
        {
            'text': 'Which mountain is the highest peak in Africa?',
            'correct_answer': 'MOUNT KILIMANJARO',
            'options': ['Mount Kenya', 'Mount Kilimanjaro', 'Mount Elgon', 'Mount Meru'],
            'difficulty_level': 1,
            'category': 'Geography'
        },
        {
            'text': 'What does HTTP stand for?',
            'correct_answer': 'HYPERTEXT TRANSFER PROTOCOL',
            'options': ['HyperText Transfer Protocol', 'High Tech Transfer Process', 'HyperText Transmission Protocol', 'Hardware Transfer Text Protocol'],
            'difficulty_level': 2,
            'category': 'Technology'
        },
        {
            'text': 'Which is the largest lake in Africa?',
            'correct_answer': 'LAKE VICTORIA',
            'options': ['Lake Victoria', 'Lake Tanganyika', 'Lake Malawi', 'Lake Chad'],
            'difficulty_level': 1,
            'category': 'Geography'
        },
        {
            'text': 'In which year was Python programming language first released?',
            'correct_answer': '1991',
            'options': ['1989', '1991', '1995', '1998'],
            'difficulty_level': 2,
            'category': 'Technology'
        },
        {
            'text': 'What is the currency of Kenya?',
            'correct_answer': 'KENYAN SHILLING',
            'options': ['Kenyan Shilling', 'Kenyan Dollar', 'East African Pound', 'Kenyan Franc'],
            'difficulty_level': 1,
            'category': 'Economics'
        },
        {
            'text': 'Which company developed the Django web framework?',
            'correct_answer': 'LAWRENCE JOURNAL-WORLD',
            'options': ['Google', 'Facebook', 'Lawrence Journal-World', 'Microsoft'],
            'difficulty_level': 3,
            'category': 'Technology'
        },
        {
            'text': 'What does SMS stand for?',
            'correct_answer': 'SHORT MESSAGE SERVICE',
            'options': ['Simple Message System', 'Short Message Service', 'Swift Messaging Service', 'Secure Message Standard'],
            'difficulty_level': 1,
            'category': 'Technology'
        },
        {
            'text': 'Which African country hosted the 2010 FIFA World Cup?',
            'correct_answer': 'SOUTH AFRICA',
            'options': ['Nigeria', 'South Africa', 'Morocco', 'Egypt'],
            'difficulty_level': 1,
            'category': 'Sports'
        },
        {
            'text': 'What is the most popular mobile money service in Kenya?',
            'correct_answer': 'M-PESA',
            'options': ['M-Pesa', 'Airtel Money', 'T-Kash', 'Equitel'],
            'difficulty_level': 1,
            'category': 'Economics'
        }
    ]
    
    print("🎯 Updated EduGame SMS Quiz Questions")
    print("=" * 60)
    print(f"Total Questions: {len(questions)}")
    
    # Count by category
    categories = {}
    difficulties = {}
    
    for q in questions:
        cat = q['category']
        diff = q['difficulty_level']
        categories[cat] = categories.get(cat, 0) + 1
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print(f"Categories: {dict(categories)}")
    print(f"Difficulty Levels: {dict(difficulties)}")
    print("\n" + "=" * 60)
    
    for i, q in enumerate(questions, 1):
        difficulty_emoji = "🟢" if q['difficulty_level'] == 1 else "🟡" if q['difficulty_level'] == 2 else "🔴"
        category_emoji = {
            'Technology': '💻',
            'Geography': '🌍', 
            'Economics': '💰',
            'Sports': '⚽'
        }.get(q['category'], '📚')
        
        print(f"\n{difficulty_emoji} Q{i} [{q['category']}] {category_emoji}")
        print(f"❓ {q['text']}")
        
        letters = ['A', 'B', 'C', 'D']
        for j, option in enumerate(q['options']):
            marker = "✅" if option.upper() == q['correct_answer'] else "  "
            print(f"   {letters[j]}) {option} {marker}")
    
    print("\n" + "=" * 60)
    print("🎮 Perfect for Hackathon Demo!")
    print("✅ Technology & Programming questions")
    print("✅ African Geography & Culture")  
    print("✅ Mixed difficulty levels")
    print("✅ Relevant to Tanzania/Kenya audience")

if __name__ == "__main__":
    display_updated_questions()