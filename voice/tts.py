from gtts import gTTS
import io

def tts_bytes(text: str, lang="ru"):
    tts = gTTS(text=text, lang=lang)
    bio = io.BytesIO()
    tts.write_to_fp(bio)
    bio.seek(0)
    return bio.read()
