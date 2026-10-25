from fastapi import FastAPI
from app.api.v1.v1 import v1_router 

app = FastAPI()

@app.get("/")
def index():
    return {"message","hello"}

@app.get("/health")
def health():
    return {"message": "healthy"}

app.include_router(v1_router, prefix="/api")

