from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    session_id: str = "default"

class Source(BaseModel):
    title: str
    section: str | None = None
    source_url: str | None = None
    score: float | None = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    intent: str
    retrieval_status: str
    memory_status: str
    confidence: float
    sources: list[Source] = []
    external_fallback_used: bool = False
