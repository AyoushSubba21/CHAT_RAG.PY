
import os
from dotenv import load_dotenv
import camelot
import pandas as pd
from langchain_community.vectorstores import FAISS
from models import get_embeddings

load_dotenv()

INDEX_PATH = "faiss_index"
PDF_FILE = "DATA/aarogya-karnataka-hospital-list-1.pdf" 
def Build_index():
    print("load the pdf...")
    #loader_txt = TextLoader("DATA/1.txt")
    #loader_pdf = PyPDFLoader("DATA/Life.pdf")
    #documents = loader_pdf.load() + loader_txt.load()

    # Split documents
    #text_splitter = RecursiveCharacterTextSplitter(
     #   chunk_size=700,
      #  chunk_overlap=80
    #)
    #chunks = text_splitter.split_documents(documents)
    print("Loading tables from PDF...")
    
    # 'lattice' flavor works for tables with visible borders..
    tables = camelot.read_pdf(PDF_FILE, pages="all", flavor="lattice")

    if not tables:
        print("No tables found in PDF.")
        return

    print(f"Found {len(tables)} tables in the PDF.")

    # Combining all tables into a single DataFrame..
    df_list = [table.df for table in tables]
    pdf_data = pd.concat(df_list, ignore_index=True)

    
    pdf_data.columns = pdf_data.iloc[0]
    pdf_data = pdf_data[1:]

    # Convert each row into a text document for embeddings..
    documents = []
    for _, row in pdf_data.iterrows():
        text = " | ".join(row.values.astype(str))
        documents.append(text)

    print(f"Converted {len(documents)} rows into documents for embeddings.")

    print("Initializing embedding model...")
    embedding_model = get_embeddings()  # your HuggingFace embedding model

    print("Building FAISS vector index...")
    vectorstore = FAISS.from_texts(documents, embedding_model)

    print("Saving FAISS index locally...")
    vectorstore.save_local(INDEX_PATH)
    print("FAISS index built successfully!")

if __name__ == "__main__":
    Build_index()
