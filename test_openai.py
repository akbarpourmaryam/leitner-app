#!/usr/bin/env python3
"""
Quick test to verify OpenAI API key works
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_key():
    """Test if OpenAI API key is configured and working"""
    
    # Check if key exists
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("\n💡 To fix:")
        print("   1. Make sure .env file exists")
        print("   2. Add: OPENAI_API_KEY=sk-your-key-here")
        return False
    
    if api_key == "PASTE_YOUR_KEY_HERE" or api_key == "your-openai-api-key-here":
        print("⚠️  You haven't replaced the placeholder API key yet!")
        print("\n💡 To fix:")
        print("   1. Get your key from: https://platform.openai.com/api-keys")
        print("   2. Edit .env file and replace with actual key")
        return False
    
    print(f"✓ API key found: {api_key[:20]}...{api_key[-4:]}")
    print("\n🧪 Testing API connection...")
    
    try:
        # Test API call
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'API test successful' in exactly 3 words"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        print("✅ API Connection Successful!")
        print(f"   Response: {result}")
        print("\n🎉 OpenAI is configured correctly!")
        print("\n💡 You can now use the 'Improve with AI' feature in your app!")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API Error: {error_msg}")
        
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            print("\n💡 Invalid API key. Please check:")
            print("   1. Copy the key correctly (starts with sk-)")
            print("   2. No extra spaces or quotes")
            print("   3. Generate a new key if needed")
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            print("\n💡 Billing issue. Please check:")
            print("   1. Your OpenAI account has credits")
            print("   2. Billing is set up at: https://platform.openai.com/account/billing")
        else:
            print("\n💡 Check your internet connection and try again")
        
        return False

if __name__ == "__main__":
    print("🔑 OpenAI API Key Test")
    print("=" * 50)
    print()
    
    success = test_openai_key()
    
    print("\n" + "=" * 50)
    
    if success:
        print("\n✅ All good! Your AI features are ready to use!")
    else:
        print("\n❌ Setup incomplete. Follow the instructions above.")

