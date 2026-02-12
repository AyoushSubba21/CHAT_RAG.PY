from build_index import Build_index
from models import get_gemini, get_embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import os
load_dotenv()

INDEX_PATH="faiss_index"
if not os.path.exists(INDEX_PATH):
    Build_index()

llm=get_gemini()
embedding_model=get_embeddings()



vectorstore=FAISS.load_local(
    INDEX_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

def Chat_response(user_input: str) -> str:

    docs=vectorstore.similarity_search(user_input,k=3)

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )

    prompt = f"""
    You are a factual assistant.

    Using ONLY the information in the context below, answer the question in 4–6 complete sentences.
    If the answer is not present, say: Not found in the documents.

    Context:
    {context}

    Question:
    {user_input}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content

