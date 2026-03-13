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
    print("Models initializing..")

    if llm is None:
        llm = get_groq()
        embedding_model = get_embeddings()
        vectorstore = FAISS.load_local(
            INDEX_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )
    print("Initializing completed")


def preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"^(who is|what is|tell me about)\s+", "", query)
    return query.strip()


PMJAY_KEYWORDS = [
    "pmjay",
    "ayushman",
    "scheme",
    "benefits",
    "eligibility",
    "apply",
    "coverage",
    "insurance",
    "health card",
]
def Chat_response(user_input: str) -> str:
    user_input = preprocess_query(user_input)

    if len(user_input.split()) < 2 and user_input not in PMJAY_KEYWORDS:
        return "I am your PMJAY Mitra. How can I help you with the Ayushman Bharat scheme today?"
    


    # Hospital search
    docs = vectorstore.similarity_search(user_input, k=5)

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )

    prompt = f"""
You are a digital assistant for Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PM-JAY).

Rules:
1. Use ONLY the information provided in the CONTEXT.
2. Do NOT invent any hospital information.
3. If the answer is not in the context, reply exactly:
"I’m sorry, I could not find relevant hospital information in the PM-JAY database."
4. Each hospital record in the context represents ONE hospital.
5. Do NOT merge hospitals.
6. Keep the SAME order as the hospitals appear in the CONTEXT.
7. Remove duplicate hospitals if any.

Return the answer ONLY in HTML format.

Format:

<p>Here are the hospitals available under PM-JAY for your query:</p>

<ol>
<li>
<b>Hospital Name</b>
<ul>
<li>Specialization: ...</li>
<li>Contact Number: ...</li>
<li>Email Id: ...</li>
<li>Address: ...</li>
</ul>
</li>
</ol>

CONTEXT:
{context}

USER QUESTION:
{user_input}
"""

    response = llm.invoke(prompt)

    return response.content
