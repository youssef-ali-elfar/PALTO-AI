from sentence_transformers import SentenceTransformer
from backend.config import settings

class EmbeddingProvider:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()

embeddings = EmbeddingProvider()
