from fastapi import APIRouter
from api.routes import messages

api_router = APIRouter()
api_router.include_router(messages.router)
