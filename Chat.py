from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
# 2. Load PDFs separately
loader_txt=TextLoader("DATA/1.txt")
loader1 = PyPDFLoader("DATA/Life.pdf")
loader2 = PyPDFLoader("DATA/DJ_History.pdf")

documents = loader1.load() + loader2.load() + loader_txt.load()
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter= RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
chunks=text_splitter.split_documents(documents)

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
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

from langchain_community.vectorstores import FAISS
vectorstore=FAISS.from_documents(chunks,embedding_model)

query="who is suryansh?"

docs=vectorstore.similarity_search(query,k=3)

print(docs[0].page_content)

