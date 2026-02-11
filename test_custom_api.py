
import os
from openai import OpenAI

# Configuration from user's manual edit
api_key="eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im5hbWUiOiJSYWplc3dhciBQIFMiLCJlbWFpbCI6InJhamVzd2FyLnN1YnJhbWFuaUBmcmVzaHdvcmtzLmNvbSIsImltYWdlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0FBUkNWSktyMjhxbU0xRTdnUE1fSlhPcDU4MEZHM2prNThMYzQ1SVB6eVFqN0lxWF89czk2LWMifSwianRpIjoiUGNVU0xxOFNrR3lYdmF1aFlEQTdsIiwiaWF0IjoxNzcwNzg2NTYwLCJleHAiOjE3NzEzOTEzNjB9.JglVKNUeldw7thE2swT0jiXKkf2M3DNUCZZ0WAIAWOg"
base_url="https://cloudverse.freshworkscorp.com/api/v1"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

print(f"Testing connection to {base_url}...")

try:
    print("Listing models...")
    models = client.models.list()
    for model in models.data:
        print(f" - {model.id}")
except Exception as e:
    print(f"Failed to list models: {e}")

try:
    print("\nAttempting completion with 'Azure-GPT-5-chat'...")
    response = client.chat.completions.create(
        model="Azure-GPT-5-chat",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("Success!")
except Exception as e:
    print(f"Failed completion: {e}")
