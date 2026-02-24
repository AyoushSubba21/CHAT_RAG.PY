import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
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

    pdf_files = [
        "DATA/treatment1.pdf",
        "DATA/GuideLines_howGovPays.pdf"
    ]
    


    all_documents = []

    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        all_documents.extend(docs)

    print(len(all_documents))

    documents = all_documents
    print("Documents loaded successfully!")

    

    print("Splitting documents...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    chunks = text_splitter.split_documents(documents)


    print("Creating embeddings...")
    embedding_model = get_embeddings();##Initializing the embedding model.....

    print("Building FAISS index...")

    vectorstore = FAISS.from_documents(chunks, embedding_model)

    print("Saving index locally...")
    vectorstore.save_local(INDEX_PATH)
    print("Index built successfully!")

if __name__ == "__main__":
    Build_index()
