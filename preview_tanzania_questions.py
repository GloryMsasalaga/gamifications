#!/usr/bin/env python3
"""
Display Tanzania-focused sample questions for EduGame SMS Quiz
"""

def display_tanzania_questions():
    """Display all the Tanzania-focused sample questions"""
    
    questions = [
        {
            'text': 'What programming language is known as the "language of the web"?',
            'correct_answer': 'JAVASCRIPT',
            'options': ['Python', 'JavaScript', 'Java', 'C++'],
            'difficulty_level': 1,
            'category': 'Technology'
        },
        {
            'text': 'What is the capital city of Tanzania?',
            'correct_answer': 'DODOMA',
            'options': ['Dar es Salaam', 'Dodoma', 'Arusha', 'Mwanza'],
            'difficulty_level': 2,
            'category': 'Tanzania Geography'
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
            'category': 'Africa Geography'
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
            'category': 'Africa Geography'
        },
        {
            'text': 'In which year was Python programming language first released?',
            'correct_answer': '1991',
            'options': ['1989', '1991', '1995', '1998'],
            'difficulty_level': 2,
            'category': 'Technology'
        },
        {
            'text': 'What is the currency of Tanzania?',
            'correct_answer': 'TANZANIAN SHILLING',
            'options': ['Tanzanian Shilling', 'Tanzanian Dollar', 'East African Pound', 'Tanzanian Franc'],
            'difficulty_level': 1,
            'category': 'Tanzania Economics'
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
            'text': 'Which is the largest city in Tanzania by population?',
            'correct_answer': 'DAR ES SALAAM',
            'options': ['Dodoma', 'Dar es Salaam', 'Mwanza', 'Arusha'],
            'difficulty_level': 1,
            'category': 'Tanzania Geography'
        },
        {
            'text': 'What is the official language of Tanzania?',
            'correct_answer': 'SWAHILI',
            'options': ['English', 'Swahili', 'Arabic', 'French'],
            'difficulty_level': 1,
            'category': 'Tanzania Culture'
        },
        {
            'text': 'Which national park in Tanzania is famous for the Great Migration?',
            'correct_answer': 'SERENGETI',
            'options': ['Ngorongoro', 'Serengeti', 'Tarangire', 'Ruaha'],
            'difficulty_level': 2,
            'category': 'Tanzania Tourism'
        }
    ]
    
    print("🇹🇿 Tanzania-Focused EduGame SMS Quiz Questions")
    print("=" * 65)
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
    print("\n" + "=" * 65)
    
    for i, q in enumerate(questions, 1):
        difficulty_emoji = "🟢" if q['difficulty_level'] == 1 else "🟡" if q['difficulty_level'] == 2 else "🔴"
        category_emoji = {
            'Technology': '💻',
            'Tanzania Geography': '🇹🇿🗺️', 
            'Tanzania Economics': '🇹🇿💰',
            'Tanzania Culture': '🇹🇿🎭',
            'Tanzania Tourism': '🇹🇿🦁',
            'Africa Geography': '🌍',
            'Sports': '⚽'
        }.get(q['category'], '📚')
        
        print(f"\n{difficulty_emoji} Q{i} [{q['category']}] {category_emoji}")
        print(f"❓ {q['text']}")
        
        letters = ['A', 'B', 'C', 'D']
        for j, option in enumerate(q['options']):
            marker = "✅" if option.upper() == q['correct_answer'] else "  "
            print(f"   {letters[j]}) {option} {marker}")
    
    print("\n" + "=" * 65)
    print("🇹🇿 Perfect for Tanzania Hackathon Demo!")
    print("✅ Technology & Programming questions")
    print("✅ Tanzania-specific geography, culture & economics")  
    print("✅ Mixed difficulty levels")
    print("✅ Highly relevant to Tanzanian audience")
    print("✅ Includes Dodoma (capital), Dar es Salaam, Swahili, Serengeti")

if __name__ == "__main__":
    display_tanzania_questions()