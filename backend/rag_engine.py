from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from pathlib import Path
import os


#load .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

#pass the openai key to the embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

#load the vectorstore
vectorstore = Chroma(persist_directory="./vector_store", embedding_function=embeddings)


#load the retriever
retriever = vectorstore.as_retriever()

#Setup RAG
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)



def get_answer(question: str, user_id: str = "guest") -> str:
    context = f"User ID: {user_id}"
    result = rag_chain.run(f"{question} | Context: {context}")
    return result


