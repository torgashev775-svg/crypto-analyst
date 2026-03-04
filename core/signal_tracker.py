from memory.chroma_store import ChromaStore
from datetime import datetime

class SignalTracker:
    def __init__(self, chroma: ChromaStore):
        self.chroma = chroma

    def record_outcome(self, analysis_id: str, outcome: dict):
        entry = {"analysis_id":analysis_id, "outcome": outcome, "date": datetime.utcnow().isoformat()}
        self.chroma.save_document(f"outcome-{analysis_id}", str(outcome), {"type":"outcome","analysis_id":analysis_id})
        return True

    def stats(self):
        items = self.chroma.query(metadata_filter={"type":"analysis"})
        total = len(items)
        wins = sum(1 for i in items if i["metadata"].get("outcome")=="win")
        return {"total": total, "wins": wins}
