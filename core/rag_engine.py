from memory.chroma_store import ChromaStore
from typing import List

class RAGEngine:
    def __init__(self, chroma: ChromaStore):
        self.chroma = chroma

    def get_relevant(self, query: str, top_k: int =5) -> List[dict]:
        results = self.chroma.find_similar(query, top_k=top_k)
        return results
