from sentence_transformers import SentenceTransformer
import numpy as np

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    vec = MODEL.encode([text], convert_to_numpy=True)[0]
    return vec / (np.linalg.norm(vec) + 1e-12)
