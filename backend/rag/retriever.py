from backend.config import settings
from backend.rag.vector_store import vector_store

def retrieve(query):
    results = vector_store.search(query, settings.top_k)
    return [r for r in results if r["score"] >= settings.min_retrieval_score]
