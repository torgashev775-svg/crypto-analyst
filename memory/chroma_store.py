import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from memory.embeddings import embed_text
import os
from typing import List

class ChromaStore:
    def __init__(self, persist_directory: str = None):
        persist_directory = persist_directory or os.getenv("CHROMA_DIR", "./data/chroma")
        self.client = chromadb.Client(Settings(chroma_db_impl="sqlite", persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection(name="crypto_analyst")

    def save_document(self, doc_id: str, text: str, metadata: dict):
        emb = embed_text(text).tolist()
        try:
            self.collection.add(doc_ids=[doc_id], metadatas=[metadata], documents=[text], embeddings=[emb])
        except Exception:
            # fallback: upsert
            self.collection.update(doc_ids=[doc_id], metadatas=[metadata], documents=[text], embeddings=[emb])

    def find_similar(self, text: str, top_k: int =5) -> List[dict]:
        emb = embed_text(text).tolist()
        try:
            results = self.collection.query(query_embeddings=[emb], n_results=top_k)
            docs = []
            for i, did in enumerate(results["ids"][0]):
                docs.append({
                    "id": did,
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "score": results["distances"][0][i]
                })
            return docs
        except Exception:
            return []

    def query(self, metadata_filter: dict = None, top_k: int = 100):
        results = self.collection.get(include=["metadatas","documents"])
        items = []
        for doc, meta in zip(results["documents"], results["metadatas"]):
            if not metadata_filter or all(meta.get(k)==v for k,v in metadata_filter.items()):
                items.append({"text":doc,"metadata":meta})
        return items
