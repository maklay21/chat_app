from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    text: str
    sender: str = "user"
    timestamp: str = None

class MessagesResponse(BaseModel):
    messages: List[Message]
