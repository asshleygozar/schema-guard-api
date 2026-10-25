from fastapi import APIRouter
from app.api.v1.routes.auth import authRouter

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(authRouter, prefix="/auth", tags=["Authentication"])

