
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

# Current working key from the code
FALLBACK_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im5hbWUiOiJSYWplc3dhciBQIFMiLCJlbWFpbCI6InJhamVzd2FyLnN1YnJhbWFuaUBmcmVzaHdvcmtzLmNvbSIsImltYWdlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0FBUkNWSktyMjhxbU0xRTdnUE1fSlhPcDU4MEZHM2prNThMYzQ1SVB6eVFqN0lxWF89czk2LWMifSwianRpIjoiTnBfQXB6MDZ3SVo4SGRGZ3RFMGMyIiwiaWF0IjoxNzcxODE5ODQwLCJleHAiOjE3NzI0MjQ2NDB9.QXTqOt-OEBfmvIanfXiQ4eTLmVXzybqYdz8758Faw5M"
FALLBACK_URL = "https://cloudverse.freshworkscorp.com/api/v1"

env_key = os.getenv("OPENAI_API_KEY")
env_url = os.getenv("OPENAI_BASE_URL")

print("--- 🔍 AOP Planner Deep Diagnostics ---")
print(f"Python: {sys.version}")
print(f"CWD: {os.getcwd()}")

api_key = env_key if env_key else FALLBACK_KEY
base_url = env_url if env_url else FALLBACK_URL

print(f"\n🔑 Key Status:")
if env_key:
    print(f"   [ENV] Using environment variable: {env_key[:10]}...{env_key[-5:]}")
else:
    print(f"   [CODE] Using internal fallback: {FALLBACK_KEY[:10]}...{FALLBACK_KEY[-5:]}")

print(f"\n📡 URL Status:")
print(f"   Using: {base_url}")

print("\n� Testing Chat Completion with model 'Azure-GPT-5-chat'...")

try:
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model="Azure-GPT-5-chat",
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        max_tokens=10
    )
    print("✨ SUCCESS! The AI replied:")
    print(f"   \"{response.choices[0].message.content}\"")
except Exception as e:
    print(f"❌ FAILED: {e}")
    if "401" in str(e):
        print("\n💡 RESOLUTION:")
        print("This is definitely an Authentication error.")
        print("1. Your session/browser might have an old cookie or your IP is restricted.")
        print("2. The key itself might be valid for SOME features but not all (unlikely).")
        print("3. IMPORTANT: Check if you have an 'OPENAI_API_KEY' exported in a different terminal.")
        print("   Try running: printenv | grep OPENAI")
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")
