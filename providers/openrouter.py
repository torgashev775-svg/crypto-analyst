import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE = "https://api.openrouter.ai/v1"  # placeholder

def call_openrouter(prompt: str, max_tokens: int=512):
    if not API_KEY:
        return None
    r = requests.post(BASE + "/responses", json={"prompt":prompt,"max_tokens":max_tokens}, headers={"Authorization":f"Bearer {API_KEY}"})
    return r.json()
