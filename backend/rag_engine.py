# RAG Engine for Document Ingestion and Retrieval
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from textblob import TextBlob

from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

VECTOR_DIR = "./vector_store"

# Check if vector DB is empty
def is_vectorstore_empty(path: str):
    return not os.path.exists(path) or not os.listdir(path)

# Ingest documents if vectorstore is empty
if is_vectorstore_empty(VECTOR_DIR):
    print("Vector store missing or empty. Ingesting documents...")

    loader = TextLoader("data/company_in.txt")
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DIR
    )
    vectorstore.persist()
    print(f"Ingested {len(chunks)} chunks.")
else:
    vectorstore = Chroma(persist_directory=VECTOR_DIR, embedding_function=embeddings)
    print(f"Loaded vectorstore with {len(vectorstore._collection.get()['documents'])} documents.")

# Set up RAG
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
llm_fallback = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

def get_fallback_response(question):
    response = llm_fallback.invoke([HumanMessage(content=question)])
    return response.content

def get_answer(question: str, user_id: str = "guest") -> str:
    # Auto-correct the question
    corrected = str(TextBlob(question).correct())
    if corrected.lower() != question.lower():
        print(f"Corrected '{question}' to '{corrected}'")
        question = corrected

    context = f"User ID: {user_id}"
    print("Running RAG on:", question)

    result = rag_chain.invoke({"query": f"{question} | Context: {context}"})

    print("RAG Result:", result)

    fallback_phrases = [
        "i don't know", "no information", "couldn't find", 
        "not enough information", "i'm sorry"
    ]

    if isinstance(result, dict):
        response = result.get("result", "")
    else:
        response = result

    if any(phrase in response.lower() for phrase in fallback_phrases):
        print("Fallback to GPT triggered.")
        return get_fallback_response(question)

    return response
