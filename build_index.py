import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from models import get_embeddings

load_dotenv()

INDEX_PATH = "faiss_index"

def Build_index():
    print("Loading documents...")

    #loader_txt = TextLoader("DATA/1.txt")
    #loader_pdf = PyPDFLoader("DATA/Treatment.pdf")
    #loader_pdf2=PyPDFLoader("DATA/DJ_HistoryAndLife.pdf")
    

    #pdf_files = [
     #   "DATA/treatment1.pdf",
      #  "DATA/HEALTH_BENEFIT_PACKAGE(HBP).pdf"
    #]
    


    #all_documents = []

   # for pdf in pdf_files:
    #    loader = PyPDFLoader(pdf)
     #   docs = loader.load()
      #  all_documents.extend(docs)

    #print(len(all_documents))

    #documents = all_documents
   # print("Documents loaded successfully!")

    

   # print("Splitting documents...")

    ##text_splitter = RecursiveCharacterTextSplitter(
      #  chunk_size=500,
       # chunk_overlap=80
    #)

    #chunks = text_splitter.split_documents(documents)
    
    csv_file = "DATA/aarogya-karnataka-hospital-list.csv" 
    
    # CSVLoader treats each row as a separate document automatically so we dont need to create chunks like in pypdf..
    loader = CSVLoader(file_path=csv_file, encoding="utf-8")
    documents = loader.load()

    print(f"Loaded {len(documents)} hospital records.")
    
    


    print("Creating embeddings...")
    embedding_model = get_embeddings();##Initializing the embedding model.....

    print("Building FAISS index...")

    vectorstore = FAISS.from_documents(documents, embedding_model)

    print("Saving index locally...")
    vectorstore.save_local(INDEX_PATH)
    print("Index built successfully!")

if __name__ == "__main__":
    Build_index()
