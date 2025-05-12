# Text-to-speech using Deepgram 

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def text_to_speech(text: str,filename: str = "output.mp3"):
    
api_key = os.getenv("DEEPGRAM_API_KEY")

#DEEPGRAM_API_URL
url= "https://api.deepgram.com/v1/speak"

header = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "text": text,
    "voice": "en-US-Wavenet-D",
    "model": "general",
    "punctuate": True,
    "encoding": "mp3"
}
response = requests.post(url, headers=header, json=payload)
if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {filename}")
else:
    print("TTS failed:" ,response.text)
    
       # print(f"Error: {response.status_code} - {response.text}")

