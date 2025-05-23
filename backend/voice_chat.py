from fastapi import APIRouter, File, UploadFile
from deepgram import Deepgram
from rag_engine import get_answer
from voice_agent import text_to_speech
from tempfile import NamedTemporaryFile
import os
import ssl
import certifi
from dotenv import load_dotenv

#  Environment setup
load_dotenv()
ssl_context = ssl.create_default_context(cafile=certifi.where())
dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

router = APIRouter()


# Used by Twilio webhook too
def process_twilio_transcript(text: str) -> str:
    try:
        return get_answer(text, user_id="caller")
    except Exception as e:
        print(" RAG error:", e)
        return "Sorry, I couldn't process that. Please try again."


#  Main endpoint for voice chat (frontend audio upload)
@router.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    output_audio_path = "output.mp3"

    # Save incoming audio to temp file
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Transcribe audio with Deepgram
        with open(tmp_path, "rb") as audio:
            source = {"buffer": audio, "mimetype": file.content_type}
            response = await dg_client.transcription.prerecorded(source, {"punctuate": True})
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            print(f"🗣️ Transcript: {transcript}")

        # Get AI answer via RAG
        ai_response = get_answer(transcript, user_id="voice_user")
        print(f" RAG Response: {ai_response}")

        # Convert to speech
        text_to_speech(ai_response, filename=output_audio_path)

        # Return JSON with details
        return {
            "transcript": transcript,
            "response": ai_response,
            "audio_file": output_audio_path
        }

    except Exception as e:
        print(" Error:", e)
        return {"error": str(e)}

    finally:
        # Clean up temp WAV file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


