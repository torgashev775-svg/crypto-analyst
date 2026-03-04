FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libjpeg-dev zlib1g-dev libpng-dev libmagic1 poppler-utils tesseract-ocr \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml* requirements.txt* /app/
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . /app
ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "webhook:app", "--host", "0.0.0.0", "--port", "8000"]