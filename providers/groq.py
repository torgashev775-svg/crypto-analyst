import os
import requests

API_KEY = os.getenv("GROQ_API_KEY")
BASE = "https://api.groq.io/v1"  # placeholder

def call_groq(prompt: str, max_tokens: int=512):
    if not API_KEY:
        return None
    # Minimal wrapper example
    r = requests.post(BASE + "/complete", json={"prompt":prompt,"max_tokens":max_tokens}, headers={"Authorization":f"Bearer {API_KEY}"})
    return r.json()
