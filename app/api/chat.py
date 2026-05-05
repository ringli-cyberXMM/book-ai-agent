from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.chatbot_service import get_reply
from app.core.security import sanitize_input

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest):
    clean_message = sanitize_input(request.message)
    reply = get_reply(request.user_id, clean_message)
    return{"reply": reply} 