

from fastapi import APIRouter, File, UploadFile
from deepgram import Deepgram
from rag_engine import get_answer
from voice_agent import text_to_speech
from tempfile import NamedTemporaryFile
import os
from dotenv import load_dotenv
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())
load_dotenv()

router = APIRouter()
dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

@router.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    # Save uploaded audio to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Transcribe audio using Deepgram
        with open(tmp_path, "rb") as audio:
            source = {"buffer": audio, "mimetype": file.content_type}
            response = await dg_client.transcription.prerecorded(source, {"punctuate": True})
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            print(f"Transcript: {transcript}")

        # Generate RAG answer
        ai_response = get_answer(transcript, user_id="voice_user")
        print(f"AI Response from RAG: '{ai_response}'")

        # Convert response to speech
        output_audio_path = "output.mp3"
        text_to_speech(ai_response, filename=output_audio_path)

        # Return the response and audio filename
        return {
            "transcript": transcript,
            "response": ai_response,
            "audio_file": output_audio_path
        }


    finally:
    # Clean up the uploaded temp WAV file
     if os.path.exists(tmp_path):
        os.remove(tmp_path)

    # Clean up the generated audio file
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

    