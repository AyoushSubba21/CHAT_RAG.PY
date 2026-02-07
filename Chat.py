from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
# 2. Load PDFs separately
loader_txt=TextLoader("DATA/1.txt")
loader1 = PyPDFLoader("DATA/Life.pdf")
##loader2 = TextLoader("DATA/DJ_HistoryAndLife.pdf")
print("Loading Documents...")
documents = loader1.load() + loader_txt.load()
print(f"Total pages loaded:{len(documents)}")

from langchain_text_splitters import RecursiveCharacterTextSplitter

print("Splitting into chunks..")
text_splitter= RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=80)
chunks=text_splitter.split_documents(documents)
print(f"Number of chunks created:{len(chunks)}")
##Alternate options for embeddings using HugginFace...

#from langchain_community.embeddings import HuggingFaceEmbeddings
#embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

##using the openAI embeddings...
#import os
#from dotenv import load_dotenv

#load_dotenv()
#api_key = os.getenv("OPENAI_API_KEY")
#embeddings=OpenAIEmbeddings(openai_api_key=api_key)

from langchain_huggingface import HuggingFaceEmbeddings
print("initializing the embedding mode...")
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})
print("Initializing done...")

print("Building the FAISS index")
from langchain_community.vectorstores import FAISS
vectorstore=FAISS.from_documents(chunks,embedding_model)
print("FAISS index built successfully...")

'''
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
print("Loading the llm model..")
llm_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",  # small model
    max_new_tokens=200,
    do_sample=False,
    temperature=0.1
)
llm=HuggingFacePipeline(pipeline=llm_pipeline)
print ("model loaded successfully...")
'''
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
print("Initializing the LLM..")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)
print("LLM initialized successfully...")

##import google.generativeai as genai
#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#print("Available models:")
#for m in genai.list_models():
 #   if 'generateContent' in m.supported_generation_methods:
  #      print(m.name)

query=str(input("Enter Your Question: "))

docs=vectorstore.similarity_search(query,k=3)

#print(docs[0].page_content)

context = "\n\n".join(
    
    f"[Source: {doc.metadata.get('source', 'Unknown')}]{doc.page_content}" for doc in docs)



prompt = f"""
You are a factual assistant.

Using ONLY the information in the context below , answer the question in 4–6 complete sentences using only the page content not the metadata.
Explain clearly and include important details.
If the answer is not present, say: Not found in the documents.

Context:
{context}

Question:
{query}

Answer:
"""



response=llm.invoke(prompt)


print("\nFinal Answer:\n")
print(response.content)
