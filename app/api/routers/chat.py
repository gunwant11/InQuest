from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services import chat_service
from app.db import get_redis_client

router = APIRouter()

class Chat(BaseModel):
    user_id: str
    message: str
    session_id: str

@router.post("/")
async def chat(chat: Chat):
    print(chat)
    response = await chat_service.handle_chat(chat)
    return response
