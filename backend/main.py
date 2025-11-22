import os
from google import genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy import text
from backend.routers import evaluate, courses, users

load_dotenv()

app = FastAPI()

# Startup event to create tables
@app.on_event("startup")
def on_startup():
    # Import Base and engine
    from backend.db.database import engine, Base
    # Import models to ensure they are registered with Base
    from backend.models import course, user
    
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if not exist).")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # ... (existing chat logic)
    pass

app.include_router(evaluate.router, prefix="/api")
app.include_router(courses.router, prefix="/api")
app.include_router(users.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
