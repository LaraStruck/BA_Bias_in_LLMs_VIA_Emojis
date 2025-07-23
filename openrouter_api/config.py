# openrouter_api/config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise EnvironmentError("API-Key nicht gefunden. Ist .env korrekt?")
    return key
