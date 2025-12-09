# app/api/v1/__init__.py
from fastapi import APIRouter
from .routes.ask import router as ask_router

api_v1_router = APIRouter()
api_v1_router.include_router(ask_router)
