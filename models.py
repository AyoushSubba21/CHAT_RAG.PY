from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()


def get_embeddings():
    embedding_model=HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device":"cpu"}
    )
    return embedding_model

def get_gemini():
    from langchain_google_genai import ChatGoogleGenerativeAI
    import os
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.2
    )
    return llm