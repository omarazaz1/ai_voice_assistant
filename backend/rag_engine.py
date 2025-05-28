
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Load the vector store
vectorstore = Chroma(persist_directory="./vector_store", embedding_function=embeddings)

# Load the retriever
retriever = vectorstore.as_retriever()

# Set up the RAG chain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Set up fallback GPT model (same model as primary)
llm_fallback = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

def get_fallback_response(question):
    response = llm_fallback([HumanMessage(content=question)])
    return response.content

def get_answer(question: str, user_id: str = "guest") -> str:
    context = f"User ID: {user_id}"
    print("Running RAG on:", question)

    result = rag_chain.run(f"{question} | Context: {context}")
    print("RAG Result:", result)

    fallback_phrases = [
        "i don't know",
        "no information",
        "couldn't find",
        "not enough information",
        "i'm sorry"
    ]

    if any(phrase in result.lower() for phrase in fallback_phrases):
        print("Fallback to GPT triggered.")
        return get_fallback_response(question)

    return result
