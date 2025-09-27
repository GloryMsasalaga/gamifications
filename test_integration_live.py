#!/usr/bin/env python3
"""
Quick Integration Test Script for Africa's Talking + ngrok
"""
import requests
import json
import sys

def test_webhook_endpoint(ngrok_url):
    """Test the SMS webhook endpoint"""
    print("🧪 Testing SMS Webhook Endpoint...")
    
    url = f"{ngrok_url}/sms/receive/"
    test_data = {
        'from': '+255628225468',  # Your phone number
        'text': 'START',
        'to': '12345',
        'id': 'test_' + str(hash('test')),
        'date': '2025-09-27 14:30:00'
    }
    
    try:
        response = requests.post(url, data=test_data, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_start_quiz_endpoint(ngrok_url):
    """Test the start quiz endpoint"""
    print("\n🎮 Testing Start Quiz Endpoint...")
    
    url = f"{ngrok_url}/start-quiz/"
    data = {'phone_number': '+255628225468'}
    
    try:
        response = requests.post(url, data=data, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_leaderboard_endpoint(ngrok_url):
    """Test the leaderboard endpoint"""
    print("\n📊 Testing Leaderboard Endpoint...")
    
    url = f"{ngrok_url}/leaderboard/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Leaderboard accessible")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

def simulate_quiz_flow(ngrok_url):
    """Simulate a complete quiz flow"""
    print("\n🎯 Simulating Complete Quiz Flow...")
    
    # Test sequence of SMS messages
    messages = [
        "START",
        "A",  # Answer first question
        "B",  # Answer second question  
        "STATUS"  # Check status
    ]
    
    webhook_url = f"{ngrok_url}/sms/receive/"
    
    for i, message in enumerate(messages, 1):
        print(f"\n📱 Step {i}: Sending '{message}'")
        
        test_data = {
            'from': '+255628225468',
            'text': message,
            'to': '12345',
            'id': f'test_flow_{i}',
            'date': '2025-09-27 14:30:00'
        }
        
        try:
            response = requests.post(webhook_url, data=test_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Response received")
                if 'response_message' in result:
                    # Show first line of response message
                    first_line = result['response_message'].split('\n')[0]
                    print(f"   📩 SMS: {first_line}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")

def main():
    print("🚀 EduGame SMS Integration Test")
    print("=" * 50)
    
    if len(sys.argv) != 2:
        print("❌ Usage: python test_integration_live.py <ngrok_url>")
        print("📝 Example: python test_integration_live.py https://abc123def.ngrok.io")
        return
    
    ngrok_url = sys.argv[1].rstrip('/')
    
    print(f"🔗 Testing URL: {ngrok_url}")
    print(f"📱 Phone: +255628225468")
    print()
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    if test_webhook_endpoint(ngrok_url):
        tests_passed += 1
        
    if test_start_quiz_endpoint(ngrok_url):
        tests_passed += 1
        
    if test_leaderboard_endpoint(ngrok_url):
        tests_passed += 1
    
    # Run quiz simulation
    simulate_quiz_flow(ngrok_url)
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Integration is working!")
        print("\n🔥 Ready for live SMS demo!")
        print("📱 Text 'START' to your Africa's Talking number")
    else:
        print("⚠️  Some tests failed. Check your setup:")
        print("   1. Is Django server running?")
        print("   2. Is ngrok tunnel active?")
        print("   3. Is the ngrok URL correct?")

if __name__ == "__main__":
    main()