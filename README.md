#  AI Voice Assistant Web App

A full-stack voice assistant that lets users speak or type to interact with an intelligent RAG-based backend, powered by OpenAI, Deepgram, and LangChain — with a sleek Next.js + ShadCN frontend.

---

## Tech Stack

| Layer        | Tools / Frameworks                                   |
|--------------|------------------------------------------------------|
| Frontend     | Next.js, Tailwind CSS, ShadCN UI                     |
| Backend      | FastAPI                                              |
| Voice Input  | Deepgram Speech-to-Text                              |
| Voice Output | Deepgram Text-to-Speech                              |
| RAG System   | LangChain + Chroma + OpenAI GPT                      |
| Storage      | Local vector store (`ChromaDB`)                      |
| Live Tunneling | Ngrok                                              |
| Audio Calls  | Twilio                                               |

---

## How It Works

1. User speaks into the app (mic input or phone call).
2. Audio is sent to the FastAPI backend.
3. The backend uses Deepgram to transcribe voice to text.
4. That text query is passed to LangChain, which retrieves relevant context from -ChromaDB-.
5. The final prompt is sent to OpenAI, which generates a response.
6. The response is turned into audio using Deepgram TTS.
7. Both the response text and generated audio are sent back to the frontend.


---

##  Features

-  Voice-to-voice interaction
-  Text chat support
-  RAG (Retrieval-Augmented Generation) powered answers
-  ShadCN UI + Tailwind styling
-  AI-generated voice replies
- Chat history stored locally
