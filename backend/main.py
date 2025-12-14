from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

from models import Message, MessagesResponse
from config.settings import settings
from redis_db import redis_client


app = FastAPI(
    title=settings.PROJECT_NAME,
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


@app.post("/api/send_message")
async def send_message(message: Message):
    """Эндпонт отправки нового сообщения"""
    try:
        if not message.timestamp:
            message.timestamp = datetime.now().isoformat()
        
        message_dict = message.dict()
        message_json = json.dumps(message_dict)
        redis_client.lpush(REDIS_CHAT_KEY, message_json)
        
        redis_client.ltrim(REDIS_CHAT_KEY, 0, 999)
        
        print(f'Send message: {message_dict}')
        return {"status": "success", "message": message_dict}
    except Exception as error:
        print(str(error))
        raise HTTPException(status_code=500, detail=str(error))
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
