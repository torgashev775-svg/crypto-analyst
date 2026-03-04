import os
from memory.chroma_store import ChromaStore
from ingestion.books import extract_text_from_file
from providers.llm_router import LLMRouter

def ingest_book(path: str, chroma: ChromaStore):
    text = extract_text_from_file(path)
    # simple chunking
    chunks = []
    words = text.split()
    size = 600
    overlap = 100
    i = 0
    while i < len(words):
        chunk_words = words[i:i+size]
        chunk_text = " ".join(chunk_words)
        meta = {"type":"book_chunk","book_title":os.path.basename(path)}
        chroma.save_document(f"book-{i}", chunk_text, meta)
        i += size - overlap
    return True
