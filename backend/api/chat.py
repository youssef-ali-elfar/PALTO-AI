from fastapi import APIRouter, HTTPException
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.chat_service import chat

router = APIRouter(prefix="/api")

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    try:
        answer, intent, status, memory_status, confidence, sources, fallback = chat(
            req.session_id, req.message
        )
        return ChatResponse(
            answer=answer,
            session_id=req.session_id,
            intent=intent,
            retrieval_status=status,
            memory_status=memory_status,
            confidence=confidence,
            sources=sources,
            external_fallback_used=fallback,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="PALTO could not process the request."
        )
