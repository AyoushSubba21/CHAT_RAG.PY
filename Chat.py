from Build_index import Build_index
from models import get_groq, get_embeddings
from extract_and_filter import extract_entities,extract_entities_no_llm,correct_with_fuzzy, post_filter,normalize_specialization
from handles_random_text import greeting_response,is_greeting,is_relevant_query,out_of_scope_response
from CONSTANT import DISTRICTS,SPECIALIZATIONS, keyword_mapping
from format import response_format
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import os
import re
import json
from rapidfuzz import process, fuzz

load_dotenv()

INDEX_PATH = "faiss_index"

if not os.path.exists(INDEX_PATH):
    Build_index()

llm = None
embedding_model = None
vectorstore = None


def initialize_models():
    global llm, embedding_model, vectorstore

    print("Models initializing...")

    #if llm is None:
     #   llm = get_groq()

    if embedding_model is None:
        embedding_model = get_embeddings()

    if vectorstore is None:
        vectorstore = FAISS.load_local(
            INDEX_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )
        print("Total documents in FAISS index:", vectorstore.index.ntotal)

    print("Initialization completed")


def preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"^(who is|what is|tell me about)\s+", "", query)
    return query.strip()


def Chat_response(user_input: str) -> str:

    user_input = preprocess_query(user_input)
    
    if is_greeting(user_input):
        return greeting_response()

    if not is_relevant_query(user_input):#if the query is not relevant to the healthcare ...
        return out_of_scope_response()
    # Extracting entities using LLM
    #entities = extract_entities(user_input,llm)
    
    #extracting entities without llm..
    entities=extract_entities_no_llm(user_input)

    district = entities.get("district")
    specialization = entities.get("specialization")
    

    # Fuzzy correction
    district = correct_with_fuzzy(district, DISTRICTS)
    specialization=normalize_specialization(specialization)#normalizing the spec before checking for fuzzy...
    specialization = correct_with_fuzzy(specialization, SPECIALIZATIONS)

    print("Detected district:", district)
    print("Detected specialization:", specialization)

    docs = vectorstore.similarity_search(user_input, k=50)
    print("Searched docs:",len(docs))

    docs = post_filter(docs, district, specialization)
    docs = docs[:10]
    print("Lata...",docs[0])
    
    print("Retrieved docs:", len(docs))

    if not docs:
        return "Sorry, I could not find any PM-JAY hospitals matching your request."

    context = "\n\n".join([doc.page_content for doc in docs])

    
    
    prompt = f"""
You are a PM-JAY hospital assistant.

IMPORTANT RULES:
1. Use ONLY the hospitals provided in the CONTEXT.
2. Do NOT create or assume hospitals.
3. If the context is empty, say:
   "No hospitals found for this query."
IMPORTANT:
- Replace "Hospital Name" with the ACTUAL hospital name from context.
- Do NOT print the words "Hospital Name".
- Use real values from the context.

Each hospital record has this format:

Hospital Name: ...
Specialization: ...
District: ...
Contact Number: ...
Email Id: ...
Address: ...

Return ONLY this HTML format:

<p>Here are the hospitals available under PM-JAY for your query:</p>

<ol>
<li>
<b>Hospital Name</b>
<ul>
<li>Specialization: ...</li>
<li>District: ...</li>
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

    #response = llm.invoke(prompt)

    #return response.content
    return response_format(docs,specialization)#Direct response without using llm....
