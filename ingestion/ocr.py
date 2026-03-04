from PIL import Image
import pytesseract
import aiohttp
import os
from loguru import logger
import io

async def ocr_from_photo(file_id: str):
    # Telegram file download requires Bot API; for now return empty or placeholder
    # In production: call getFile and download file, run pytesseract
    logger.debug("OCR requested for file_id {}", file_id)
    return ""

def ocr_image_bytes(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(img, lang="eng+rus")
    return text
