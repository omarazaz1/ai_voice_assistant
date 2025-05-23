
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

def text_to_speech(text: str, filename: str = "output.mp3"):
    api_key = os.getenv("DEEPGRAM_API_KEY")

    if not api_key:
        raise ValueError("Missing DEEPGRAM_API_KEY")

    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en&encoding=mp3"  #  PASS model & encoding as query params

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text  # ONLY this is required in JSON
    }

    print(" Sending TTS request with:", payload)

    response = requests.post(url, headers=headers, json=payload)

    print(" Deepgram TTS response:", response.status_code, response.text[:200])

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f" Audio saved as {filename}")
    else:
        raise RuntimeError(f"TTS failed: {response.status_code} {response.text}")
