
import os
import json

# Mimic app.py setup
ROADMAP_DATA_DIR = 'data'
USERS_FILE = os.path.join(ROADMAP_DATA_DIR, 'users.json')

def get_users():
    print(f"Checking for users file at: {os.path.abspath(USERS_FILE)}")
    if os.path.exists(USERS_FILE):
        print("File found.")
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    else:
        print("File NOT found.")
    return []

def api_login(username, password):
    users = get_users()
    print(f"Users found: {len(users)}")
    user_data = next((u for u in users if u['username'] == username and u['password'] == password), None)
    
    if user_data:
        print("Login SUCCESS")
        return True
    else:
        print("Login FAILED")
        return False

# Test with credentials from the file
print("--- Testing Admin Login ---")
api_login("admin", "adminpassword")

print("\n--- Testing User Login ---")
api_login("user", "userpassword")
