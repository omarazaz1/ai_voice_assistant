from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Initialize FastAPI
app = FastAPI()

# Import routes
from rag_engine import get_answer
from voice_chat import router as voice_router
from twilio_webhook import router as twilio_router

# Register routes
app.include_router(voice_router)
app.include_router(twilio_router)

# CORS config for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    
    
)

# @app.post("/")
# async def root_post():
#     return {"message": "This endpoint only supports GET or is not used."}
from fastapi import status
@app.post("/")
async def root_post():
    return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content={"error": "POST not allowed here."})


@app.get("/")
def read_root():
    return {"message": "Omar AI Voice Assistant API is running Thank you for testing!"}

@app.get("/test-openai")
async def test_openai():
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
        response = llm.invoke("Say hello from ChatGPT")
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/audio")
def get_audio():
    audio_path = "output.mp3"
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    else:
        return JSONResponse(status_code=404, content={"error": "Audio not found"})

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        question = body.get("question", "")
        user_id = body.get("user_id", "guest")

        print(" RAG Question:", question)
        
        

        answer = get_answer(question, user_id)
        return {"response": answer}
    except Exception as e:
        print("RAG ERROR:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
