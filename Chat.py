from build_index import Build_index
from models import get_embeddings, get_groq
from langchain_huggingface import HuggingFaceEmbeddings
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
        llm = get_groq()
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
    initialize_models()
    user_input = preprocess_query(user_input)

    if len(user_input.split()) < 2 and user_input not in PMJAY_KEYWORDS:
        return "I am your PMJAY Mitra. How can I help you with the Ayushman Bharat scheme today?"
    
    # PMJAY explanation mode
    if any(word in user_input for word in PMJAY_KEYWORDS):

        prompt = f"""
You are a healthcare assistant explaining Ayushman Bharat (PM-JAY).

Explain clearly:
- What PMJAY is
- Benefits
- Eligibility
- Coverage amount
- How to apply

Return answer in simple HTML format.

User Question:
{user_input}
"""

        response = llm.invoke(prompt)
        return response.content


    # Hospital search
    if len(user_input.split()) < 2 and user_input not in ["benefits", "eligibility", "treatment"]:
        return "I am your PMJAY Mitra. How can I help you with the Ayushman Bharat scheme today?"

    docs = vectorstore.similarity_search(user_input, k=5)

    if not docs:
        return "I am PMJAY Bot ask me regarding to it!!. Like Which hospital provides what ?"

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )


    prompt = f"""
You are an official digital assistant for the Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PM-JAY).

STRICT RULES:
1. Answer ONLY using the information provided in the CONTEXT.
2. If the answer cannot be found in the context, reply EXACTLY with:
"I’m sorry, I could not find relevant information in the available records in our PMJAY Hospital list."
3. Understand small spelling mistakes in the user's query.
4. If a specialization is mentioned, return ONLY hospitals that match that specialization.
5. Remove duplicate hospitals.
6. Return the response ONLY in HTML format.
7. Hospitals must be indexed starting from 1.

Professional Behaviour Rules:
1. Respond politely and professionally like a government digital assistant.
2. If the user greets you (hello, hi, etc.), respond politely and ask how you can help.
3. Answer questions about PM-JAY benefits, eligibility, hospitals, and treatments.
4. Use ONLY the information provided in CONTEXT when listing hospitals.
5. If no relevant hospital information exists in the context, say:

"I’m sorry, I could not find relevant hospital information in the PM-JAY database."

6. Return hospital results in structured HTML format.

HTML RESPONSE FORMAT:

Start with a short introduction.

Then list hospitals using this exact structure:

Then list hospitals using this exact structure:

<br>
1. <b>hospital_name</b><br>
<ul>
<li>Specialization: matching_specialization</li>
<li>Contact Number: contact_number</li>
<li>Address: address</li>
</ul>

<br>

Continue numbering sequentially.

CONTEXT:
{context}

USER QUESTION:
{user_input}
"""

    response = llm.invoke(prompt)

    return response.content
