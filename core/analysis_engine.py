import asyncio
from loguru import logger
from memory.chroma_store import ChromaStore
from ingestion.ocr import ocr_from_photo
from ingestion.twitter import fetch_tweet_text
from core.rag_engine import RAGEngine
from providers.llm_router import LLMRouter
from datetime import datetime
import json

class AnalysisEngine:
    def __init__(self, queue: asyncio.Queue, chroma: ChromaStore):
        self.queue = queue
        self.chroma = chroma
        self.rag = RAGEngine(chroma)
        self.llm = LLMRouter()
        self.sem = asyncio.Semaphore(3)

    async def worker(self):
        while True:
            post = await self.queue.get()
            try:
                async with self.sem:
                    await self.process_post(post)
            except Exception as e:
                logger.exception("worker error: {}", e)
            finally:
                self.queue.task_done()

    async def process_post(self, post: dict):
        msg_id = post.get("message_id")
        text = post.get("text") or post.get("caption") or ""
        entities = post.get("entities", [])
        # extract urls
        urls = []
        for ent in entities:
            if ent.get("type") == "url":
                offset = ent["offset"]
                length = ent["length"]
                urls.append(text[offset:offset+length])
        # media: photos, voice, documents
        media_text = ""
        if post.get("photo"):
            # take last photo (biggest)
            photo = post["photo"][-1]
            file_id = photo["file_id"]
            try:
                media_text = await ocr_from_photo(file_id)
            except Exception:
                media_text = ""
        # twitter links
        for u in urls:
            if "twitter.com" in u or "x.com" in u:
                tweet = await fetch_tweet_text(u)
                if tweet:
                    text += "\n\n[TWEET]\n" + tweet
        # RAG retrieval
        rag_ctx = self.rag.get_relevant(text, top_k=5)
        # dedup check
        similar = self.chroma.find_similar(text, top_k=1)
        if similar and similar[0].get("score", 1.0) > 0.92:
            logger.info("Dedup detected for msg {}", msg_id)
            return similar[0]["metadata"].get("analysis_id")
        # build prompt
        prompt = f"Post:\n{text}\n\nContext:\n{''.join([r['text'] for r in rag_ctx])}"
        response = await self.llm.analyze(prompt, max_tokens=800)
        analysis = {
            "analysis_id": f"analysis-{msg_id}-{int(datetime.utcnow().timestamp())}",
            "date": datetime.utcnow().isoformat(),
            "source": "telegram",
            "coin": response.get("coin"),
            "sentiment": response.get("sentiment"),
            "tag": response.get("tag"),
            "type": "analysis",
            "text": text,
            "analysis": response,
        }
        self.chroma.save_document(analysis["analysis_id"], text, analysis)
        logger.info("Saved analysis {}", analysis["analysis_id"])
        return analysis["analysis_id"]
