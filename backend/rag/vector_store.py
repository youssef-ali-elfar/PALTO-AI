import chromadb
from backend.config import settings
from backend.rag.embeddings import embeddings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.vector_db_path)
        self.collection = self.client.get_or_create_collection(
            name="palto_medical",
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, records):
        if not records:
            return
        self.collection.upsert(
            ids=[r["id"] for r in records],
            documents=[r["text"] for r in records],
            metadatas=[
                {k: str(v) for k, v in r.items() if k not in {"id", "text"}}
                for r in records
            ],
            embeddings=embeddings.embed([r["text"] for r in records]),
        )

    def search(self, query, k=5):
        if self.collection.count() == 0:
            return []
        result = self.collection.query(
            query_embeddings=[embeddings.embed_query(query)],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
        output = []
        for i, text in enumerate(result["documents"][0]):
            distance = float(result["distances"][0][i])
            output.append({
                "text": text,
                "score": max(0.0, 1.0 - distance),
                "metadata": result["metadatas"][0][i] or {},
            })
        return output

vector_store = VectorStore()
