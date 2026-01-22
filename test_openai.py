
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key present: {bool(api_key)}")

try:
    client = OpenAI(api_key=api_key)
    print("Success")
except Exception as e:
    print(f"Failed: {e}")
