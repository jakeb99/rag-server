from fastapi import APIRouter
from app.api.v1.endpoints import document_upload

api_router = APIRouter()
api_router.include_router(document_upload.router)