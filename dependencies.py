import os
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI

# Load env vars
load_dotenv()

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
ROADMAP_FILE = DATA_DIR / "roadmaps.json"
USERS_FILE = DATA_DIR / "users.json"
FORM_CONFIG_FILE = DATA_DIR / "roadmap_form.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "roadmap_attachments").mkdir(exist_ok=True)
if not ROADMAP_FILE.exists():
    ROADMAP_FILE.write_text("[]")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aop_planner")

# Templates
templates = Jinja2Templates(directory="templates")

# OpenAI Client
class LLMClient:
    def __init__(self):
        self.client = None
        self.available = False
        try:
            # Using specific key/url from original app.py if env var not set, 
            # though best practice is env vars. Keeping original logic for compatibility.
            api_key = os.getenv("OPENAI_API_KEY", "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im5hbWUiOiJSYWplc3dhciBQIFMiLCJlbWFpbCI6InJhamVzd2FyLnN1YnJhbWFuaUBmcmVzaHdvcmtzLmNvbSIsImltYWdlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0FBUkNWSktyMjhxbU0xRTdnUE1fSlhPcDU4MEZHM2prNThMYzQ1SVB6eVFqN0lxWF89czk2LWMifSwianRpIjoiT3NOSUtEVVdiaHhjSElvZHNMNXFEIiwiaWF0IjoxNzY5OTI3MTA3LCJleHAiOjE3NzA1MzE5MDd9.WASBTxcAlJhAjWlzdz4Myfa3DRdO8JdlLZsArUuMt10")
            base_url = os.getenv("OPENAI_BASE_URL", "https://cloudverse.freshworkscorp.com/api/v1")
            
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.available = True
            logger.info("OpenAI client initialized")
        except Exception as e:
            logger.error(f"Failed to init OpenAI: {e}")

llm_service = LLMClient()

def get_llm_client():
    return llm_service.client

def get_templates():
    return templates

# Data Access Helpers
def get_users_data() -> List[Dict]:
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text())
        except Exception as e:
            logger.error(f"Error reading users: {e}")
    return []

def save_users_data(users: List[Dict]):
    USERS_FILE.write_text(json.dumps(users, indent=2))

def get_roadmaps_data() -> List[Dict]:
    if ROADMAP_FILE.exists():
        try:
            return json.loads(ROADMAP_FILE.read_text())
        except:
            return []
    return []

def save_roadmaps_data(data: List[Dict]):
    ROADMAP_FILE.write_text(json.dumps(data, indent=2))
