from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import redis
import json

from models import Message, MessagesResponse


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

REDIS_CHAT_KEY = "chat:messages"


@app.get("/")
def home():
    return {"status": "Chat API is running"}


@app.get("/api/messages", response_model=MessagesResponse)
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
        print(str(error))
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/api/messages")
async def create_message(message: Message):
    """Эндпонт создания нового сообщения"""
    try:
        if not message.timestamp:
            message.timestamp = datetime.now().isoformat()
        
        message_dict = message.dict()
        message_json = json.dumps(message_dict)
        redis_client.lpush(REDIS_CHAT_KEY, message_json)
        
        redis_client.ltrim(REDIS_CHAT_KEY, 0, 999)
        
        print(f'Create message: {message_dict}')
        return {"status": "success", "message": message_dict}
    except Exception as error:
        print(str(error))
        raise HTTPException(status_code=500, detail=str(error))
