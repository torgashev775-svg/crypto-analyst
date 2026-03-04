import os
import requests

API_KEY = os.getenv("WHISPER_API_KEY")

def transcribe_bytes(audio_bytes: bytes):
    if API_KEY:
        # call provider
        return ""
    # fallback: not implemented
    return ""
