from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# No need to import openai directly anymore
from rag_engine import get_answer  # NEW: Import our RAG engine

from voice_chat import router as voice_router
app.include_router(voice_router)



# Load environment variables
load_dotenv()

app = FastAPI()

#  Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Voice Assistant API is running!"}

#  Updated /chat endpoint to use RAG
@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        question = body.get("question", "")
        user_id = body.get("user_id", "guest")

        print("🔍 RAG Question:", question)

        # Use your embedded knowledge base to get an answer
        answer = get_answer(question, user_id)

        return {"response": answer}

    except Exception as e:
        print("RAG ERROR:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
