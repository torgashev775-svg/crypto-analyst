import pdfplumber
import os

def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = []
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                text.append(p.extract_text() or "")
        return "\n".join(text)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
