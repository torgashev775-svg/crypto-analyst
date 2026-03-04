import asyncio
from providers import groq, deepseek, openrouter, xai
from loguru import logger

class LLMRouter:
    def __init__(self):
        self.chain = [groq, deepseek, openrouter, xai]

    async def analyze(self, prompt: str, max_tokens: int=800):
        loop = asyncio.get_event_loop()
        for provider in self.chain:
            try:
                fn = getattr(provider, f"call_{provider.__name__}")
            except Exception:
                # fallback generic
                fn = getattr(provider, list(filter(lambda x: x.startswith("call_"), dir(provider)))[0], None)
            if not fn:
                continue
            try:
                resp = await loop.run_in_executor(None, lambda: fn(prompt, max_tokens))
                if resp:
                    # Expect provider to return text; normalize
                    text = resp.get("text") if isinstance(resp, dict) else str(resp)
                    # Minimal parse into fields
                    return {"raw": text, "coin": None, "sentiment": "neutral", "tag": None}
            except Exception as e:
                logger.warning("provider {} failed: {}", provider, e)
        # fallback: simple heuristic
        return {"raw": prompt[:400], "coin": None, "sentiment": "neutral", "tag": None}
