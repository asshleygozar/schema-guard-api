from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.v1 import v1_router
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
)

@app.get("/")
def index():
    return {"message","hello"}

@app.get("/health")
def health():
    return {"message": "healthy"}

app.include_router(v1_router, prefix="/api")
