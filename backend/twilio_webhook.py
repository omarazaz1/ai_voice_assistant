from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from voice_chat import process_twilio_transcript

router = APIRouter()

@router.post("/twilio-voice")
async def twilio_voice(request: Request):
    form = await request.form()
    speech_result = form.get("SpeechResult")

    response = VoiceResponse()

    if speech_result:
        print("📞 User said:", speech_result)
        ai_response = process_twilio_transcript(speech_result)
        print("🤖 AI Response:", ai_response)
        response.say(ai_response, voice="alice")
    else:
        # Ask the caller a question using <Gather>
        gather = Gather(input='speech', action='/twilio-voice', method='POST', timeout=5)
        gather.say("Welcome to your AI assistant. What would you like to ask?")
        response.append(gather)
        response.redirect('/twilio-voice')  # if nothing captured, ask again

    return Response(content=str(response), media_type="application/xml")
