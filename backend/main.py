
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse, JSONResponse #just added 

import os


from rag_engine import get_answer  # RAG engine
from voice_chat import router as voice_router

from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from .env file


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


app = FastAPI()



from langchain_openai import ChatOpenAI #temporary import

@app.get("/test-openai")
async def test_openai():
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
        response = llm.invoke("Say hello from ChatGPT")
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}



# Include the voice router
app.include_router(voice_router)

# CORS config for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
   return {"message": "Omar AI Voice Assistant API is running Thank you for testing !"}
   
@app.get("/audio")  # Added endpoint to serve audio
def get_audio():
    audio_path = "output.mp3"
    if os.path.exists(audio_path):
        #  Serve the generated audio file
        return FileResponse(audio_path, media_type="audio/mpeg")
    else:
        # Handle file not found error
        return JSONResponse(status_code=404, content={"error": "Audio not found"}) # end


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
