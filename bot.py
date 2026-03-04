import aiohttp
import asyncio
from loguru import logger
from config import TELEGRAM_BOT_TOKEN

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

async def send_message(chat_id: int, text: str, parse_mode="Markdown"):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()
            if not data.get("ok"):
                logger.error("Failed to send message: {}", data)
            return data

async def send_voice(chat_id: int, voice_bytes: bytes):
    url = f"{BASE_URL}/sendVoice"
    data = aiohttp.FormData()
    data.add_field("chat_id", str(chat_id))
    data.add_field("voice", voice_bytes, filename="voice.ogg", content_type="audio/ogg")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            return await resp.json()
