import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.routers import evaluate, courses

load_dotenv()

app = FastAPI()

# Startup event to create tables
@app.on_event("startup")
def on_startup():
    # Import Base and engine
    from backend.db.database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if not exist).")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=request.prompt
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(evaluate.router, prefix="/api")
app.include_router(courses.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
