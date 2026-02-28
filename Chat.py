from build_index import Build_index
from models import get_gemini, get_embeddings, get_groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import os
import re  # for preprocessing the query..

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

    if len(user_input.split()) < 2 and user_input not in [ "benefits", "eligibility", "treatment"]:
        return "I am your PMJAY Mitra. How can I help you with the Ayushman Bharat scheme today?"

    docs = vectorstore.similarity_search(user_input, k=7)

    if not docs:
        return "I am PMJAY Bot ask me regarding to it!!. Like Which hospital provides what ?"

    context = "\n\n".join(
        f"[Source] {doc.page_content}" for doc in docs
    )

    prompt = f"""
You are a professional healthcare assistance chatbot for Ayushman Bharat (PM-JAY).

GUIDELINES:
1. Use ONLY the information provided in the CONTEXT section.
2. Do NOT provide any information that is not present in the context.
3. If the answer cannot be found in the context, reply:
   "I’m sorry, I could not find relevant information in the available records."
4. Do NOT copy text verbatim from the context; always rephrase clearly and professionally.
5. Remove duplicates and redundant information.
6. Keep the response concise, clear, and well-structured.
7. Understand and correctly interpret user queries even if there are minor spelling mistakes, typos, or slight grammatical errors.
8. Provide responses in a professional and reader-friendly manner.

ANSWER FORMAT:
1. Start with a brief introduction about the topic. For example, if the user asks "What are the hospitals for eye treatment?", begin with: "These are the hospitals that provide eye treatment."
2. Use bold headings for each key item, e.g., Hospital Name.
3. Ensure proper spacing between lines and sections for readability.
4. Present information in a structured manner with clear bullet points or short paragraphs.

CONTEXT:
{context}

USER QUESTION:
{user_input}

Provide the final structured and professional answer below:
"""

    response = llm.invoke(prompt)

    return response.content