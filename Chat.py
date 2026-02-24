
from build_index import Build_index
from models import get_gemini, get_embeddings,get_groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import os
import re#for preprocessing the query..
load_dotenv()

INDEX_PATH="faiss_index"
if not os.path.exists(INDEX_PATH):
    Build_index()


llm=None;
embedding_model=None;
vectorstore=None;
print("lata")
def initialize_models():
    global llm, embedding_model, vectorstore

    if llm is None:
        llm=get_groq()
        embedding_model=get_embeddings()
        vectorstore=FAISS.load_local(
            INDEX_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )


def preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"^(who is|what is|tell me about)\s+", "", query)
    return query.strip()
def Chat_response(user_input: str) -> str:
    initialize_models()
    user_input=preprocess_query(user_input)

    if len(user_input.split()) < 2 and user_input not in ["apply", "benefits", "eligibility","treatment"]:
        return "I am your Digital Mitra. How can I help you with the Ayushman Bharat scheme today?"

    docs=vectorstore.similarity_search(user_input,k=3)

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )

    prompt = f"""
    You are a factual assistant.

    INSTRUCTIONS:
    1. Use ONLY the provided Context to answer the Question.
    2. If the user asks about people (e.g., 'Who is Ghora?'), search the Context for that specific name or keyword.
    3. If the information is in the context, provide a detailed answer.
    4. If the answer is truly not in the context, say: "I apologize, but I could not find information regarding this in the official PM-JAY records."

    CRITICAL INSTRUCTION: 
    - You must ignore case-sensitivity (UPPERCASE or lowercase does not matter).
    -You may get data where only small part of the query is used, so you must be able to understand the query and provide answer based on the context..

    Context:
    {context}

    Question:
    {user_input}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content