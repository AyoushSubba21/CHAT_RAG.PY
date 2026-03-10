from build_index import Build_index
from models import get_gemini, get_embeddings, get_groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import os
import re

load_dotenv()

INDEX_PATH = "faiss_index"

if not os.path.exists(INDEX_PATH):
    Build_index()

llm = None
embedding_model = None
vectorstore = None

print("lata")


def initialize_models():
    global llm, embedding_model, vectorstore

    if llm is None:
        llm = get_gemini()
        embedding_model = get_embeddings()
        vectorstore = FAISS.load_local(
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

    user_input = preprocess_query(user_input)

    docs = vectorstore.similarity_search(user_input, k=5)

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )

    prompt = f"""
You are an official digital assistant for the Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PM-JAY).

Your role is to help citizens with:
• Scheme benefits
• Eligibility criteria
• Covered treatments
• PM-JAY empanelled hospitals

Professional Behaviour Rules:
1. Respond politely and professionally like a government digital assistant.
2. If the user greets you (hello, hi, etc.), respond politely and ask how you can help.
3. Answer questions about PM-JAY benefits, eligibility, hospitals, and treatments.
4. Use ONLY the information provided in CONTEXT when listing hospitals.
5. If no relevant hospital information exists in the context, say:

"I’m sorry, I could not find relevant hospital information in the PM-JAY database."

6. Return hospital results in structured HTML format.

HTML FORMAT:

Start with a short introduction.

<br>

1. <b>Hospital Name</b><br>
<ul>
<li>Specialization: ...</li>
<li>Contact Number: ...</li>
<li>Address: ...</li>
</ul>

Leave one blank line between hospitals.

CONTEXT:
{context}

USER QUESTION:
{user_input}

Provide the final answer below.
"""

    response = llm.invoke(prompt)

    return response.content