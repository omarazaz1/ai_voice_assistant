# Full voice interaction handler: audio -> transcript -> response -> speech
importos
from fastapi import APIRouter,file, UploadFile
from deepgram import Deepgram
from rag_engine import get_answer
from voice_agent import text_to_speech
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv


load_dotenv()
# Initialize Deepgram client

dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
router = APIRouter()

@router.post("/voice_chat")
async def voice_chat(file: UploadFile = File(...)):
    
    #save the uploaded file to a temporary location
    with NamedTemporaryFile(delete= False , suffix  = ".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
       # print(f"Temporary file saved at: {tmp_path}")
       
# Transcribe using Deepgram

    with open(tmp_path, "rb") as audio:
        source = {"buffer": audio, "mimetype": file.content_type}
        response = await dg_client.transcription.prerecorded(source, {"punctuate": True})
        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(f"Response: {transcript}")
        
    # Get answer using RAG
    ai_response = get_answer(transcript, user_id="voice_user")
    print("AI Response: {ai_response}")
    
    #convert text to speech
    text_to_speech(ai_response, filename="output.mp3")
    return {"transcript": transcript,
            "ai_response": ai_response,
            "audio_file": "output.mp3"}
    
    
    #cleanup the temporary file(optional)
    os.remove(tmp_path)

            
       
        
        