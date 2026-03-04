import os
import requests

API_KEY = os.getenv("XAI_API_KEY")
BASE = "https://api.grok.x.ai/v1"  # placeholder

def call_xai(prompt: str, max_tokens: int=512):
    if not API_KEY:
        return None
    r = requests.post(BASE + "/complete", json={"prompt":prompt,"max_tokens":max_tokens}, headers={"Authorization":f"Bearer {API_KEY}"})
    return r.json()
