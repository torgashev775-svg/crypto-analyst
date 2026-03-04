from fastapi import FastAPI, Request, HTTPException
import asyncio
from loguru import logger
import os
from config import TELEGRAM_BOT_TOKEN, ALLOWED_CHANNEL_ID, WEBHOOK_PATH, MAX_CONCURRENT_ANALYSES, LOG_LEVEL
from core.analysis_engine import AnalysisEngine
from memory.chroma_store import ChromaStore
from storage.s3 import S3Sync

logger.remove()
logger.add("logs/bot.log", rotation="5 MB", level=LOG_LEVEL)

app = FastAPI()
queue: asyncio.Queue = asyncio.Queue()
engine = AnalysisEngine(queue=queue, chroma=ChromaStore())
s3sync = S3Sync()

async def _periodic_push(interval: int = 600):
    loop = asyncio.get_event_loop()
    local_dir = os.getenv("CHROMA_DIR", "./data/chroma")
    while True:
        await asyncio.sleep(interval)
        try:
            await loop.run_in_executor(None, lambda: s3sync.upload_dir(local_dir))
            logger.info("Periodic chroma upload to S3 completed")
        except Exception:
            logger.exception("Periodic S3 upload failed")

@app.on_event("startup")
async def startup():
    logger.info("Starting startup tasks")
    # pull chroma from S3 on startup
    local_dir = os.getenv("CHROMA_DIR", "./data/chroma")
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, lambda: s3sync.download_dir(local_dir))
        logger.info("Chroma pulled from S3 to %s", local_dir)
    except Exception:
        logger.exception("Failed pulling chroma from S3")
    # start workers
    for _ in range(MAX_CONCURRENT_ANALYSES):
        asyncio.create_task(engine.worker())
    # start periodic push task
    asyncio.create_task(_periodic_push(600))

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    # Basic validation
    if "channel_post" not in data:
        raise HTTPException(status_code=400, detail="Only channel_post supported")
    post = data["channel_post"]
    chat = post.get("chat", {})
    chat_id = chat.get("id")
    if ALLOWED_CHANNEL_ID and chat_id != ALLOWED_CHANNEL_ID:
        raise HTTPException(status_code=403, detail="Forbidden channel")
    await queue.put(post)
    logger.info("Enqueued post id={}", post.get("message_id"))
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webhook:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
