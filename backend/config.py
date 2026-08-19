from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_api_key: str = ""
    llm_base_url: str = "https://api.tokenbay.com/v1/messages"
    llm_model: str = "claude-opus-4.7"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    vector_db_path: str = "./data/chroma"
    top_k: int = 5
    min_retrieval_score: float = 0.35
    max_memory_messages: int = 10

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
