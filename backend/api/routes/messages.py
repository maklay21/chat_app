from fastapi import FastAPI, APIRouter, HTTPException
from datetime import datetime
import json

from config.logging_config import logger
from models import Message, MessagesResponse
from config.settings import settings
from redis_db import redis_client


router = APIRouter(prefix="/messages", tags=["messages"])
REDIS_CHAT_KEY = "chat:messages"


@router.get("", response_model=MessagesResponse)
@router.get("/", response_model=MessagesResponse)
async def get_messages():
    """Эндпонт получения всех сообщений"""
    try:
        messages = redis_client.lrange(REDIS_CHAT_KEY, 0, -1)
        if not messages:
            return MessagesResponse(messages=[])
        
        messages_json = []
        for msg in messages:
            msg_json = json.loads(msg)
            messages_json.append(Message(**msg_json))
        
        return MessagesResponse(messages=messages_json)
    except Exception as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/send_message")
async def send_message(message: Message):
    """Эндпонт отправки нового сообщения"""
    try:
        if not message.timestamp:
            message.timestamp = datetime.now().isoformat()
        
        message_dict = message.dict()
        message_json = json.dumps(message_dict)
        redis_client.lpush(REDIS_CHAT_KEY, message_json)
        
        logger.info(f'Send message: {message_dict}')
        return {"status": "success", "message": message_dict}
    except Exception as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error))
