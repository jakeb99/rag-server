from fastapi import APIRouter
from app.api.v1.endpoints import document_upload
from app.api.v1.endpoints import test

api_router = APIRouter()
api_router.include_router(document_upload.router)
api_router.include_router(test.router)