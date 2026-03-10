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

    if len(user_input.split()) < 2 and user_input not in ["benefits", "eligibility", "treatment"]:
        return "I am your PMJAY Mitra. How can I help you with the Ayushman Bharat scheme today?"

    docs = vectorstore.similarity_search(user_input, k=5)

    if not docs:
        return "I am PMJAY Bot ask me regarding to it!!. Like Which hospital provides what ?"

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )


    prompt = f"""
You are a professional healthcare assistance chatbot for Ayushman Bharat (PM-JAY).

STRICT RULES:
1. Answer ONLY using the information provided in the CONTEXT.
3. If the answer cannot be found in the context, reply EXACTLY with:
"I’m sorry, I could not find relevant information in the available records in our PMJAY Hospital list."
4. Understand small spelling mistakes in the user's query.
5. If a specialization is mentioned, return ONLY hospitals that match that specialization.
6. Remove duplicate hospitals.
7. Return the response ONLY in HTML format exactly as defined below.

HTML RESPONSE FORMAT:

Start with a short introduction.

Then list hospitals using this exact structure:

<br>
<Use numbered list starting from 1.>. <b>hospital_name</b><br>
<ul>
    <li>Specialization: matching_specialization</li>
    <li>Contact Number: contact_number</li>
    <li>Address: address</li>
</ul>

<br>

Leave exactly ONE blank line between hospitals.

CONTEXT:
{context}

USER QUESTION:
{user_input}

Provide the final structured answer below:
"""

    response = llm.invoke(prompt)

    return response.content
