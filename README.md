# Crypto Analyst Bot

Telegram admin-agent that analyzes forwarded posts in a private channel with deep crypto/trading reasoning, RAG over uploaded books, voice transcription, OCR, market enrichment and outcome tracking. Ready for GitHub and Render.com deployment.

Getting started
1. Copy `.env.example` to `.env` and fill keys.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Run locally: `uvicorn webhook:app --host 0.0.0.0 --port 8000`
4. Set Telegram webhook:
   - URL: `${WEBHOOK_BASE_URL}${WEBHOOK_PATH}`
   - Use `https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook?url=${WEBHOOK_BASE_URL}${WEBHOOK_PATH}`
5. Make your bot admin in the private channel.

Render deployment
1. Create a new Web Service on Render (Python).
2. Add environment variables from your `.env`.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn webhook:app --host 0.0.0.0 --port $PORT`
5. Use UptimeRobot to ping your service URL periodically to avoid sleeps.

Notes
- Place persistent chroma data in `data/chroma`.
- Logs are in `logs/bot.log`.
- See commands: `/tags`, `/list_tags`, `/books`, `/book_summary`, `/patterns`, `/stats`.

License: MIT
