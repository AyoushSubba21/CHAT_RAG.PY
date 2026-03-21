import os
from dotenv import load_dotenv
import camelot
import pandas as pd
from langchain_community.vectorstores import FAISS
from models import get_embeddings
from langchain_core.documents import Document

load_dotenv()

INDEX_PATH = "faiss_index"
PDF_FILE = "DATA/aarogya-karnataka-hospital-list-1.pdf"

def Build_index():
    print("Loading tables from PDF...")

    # Use lattice or stream depending on PDF structure
    try:
        tables = camelot.read_pdf(PDF_FILE, pages="1-40", flavor="lattice")
    except Exception as e:
        print(f"Error reading PDF with lattice: {e}, trying stream...")
        tables = camelot.read_pdf(PDF_FILE, pages="1-50", flavor="stream")

    if not tables:
        print("No tables found in PDF.")
        return

    print(f"Found {len(tables)} tables in the PDF.")

    # Combine all tables, skip empty ones
    df_list = [table.df for table in tables if not table.df.empty]
    pdf_data = pd.concat(df_list, ignore_index=True)

    # Set correct column names
    pdf_data.columns = [
        "sl_no",
        "hospital_name",
        "address",
        "district",
        "taluk",
        "division",
        "ownership",       # govt/private
        "contact_number",
        "email_id",
        "scheme",
        "speciality"
    ]

    # Remove the first row if it contains repeated headers
    pdf_data = pdf_data[1:].reset_index(drop=True)

    # Clean empty values
    pdf_data = pdf_data.replace(r'^\s*$', pd.NA, regex=True)
    pdf_data = pdf_data.fillna("No Name")

    print(f"Total rows after cleaning: {len(pdf_data)}")

    # Convert each valid row into a document
    documents = []
    skipped_rows = 0
    
    for _, row in pdf_data.iterrows():
        hospital = str(row.get("hospital_name", "")).strip()
        specialization = str(row.get("speciality", "")).strip()
        district = str(row.get("district", "")).strip()
        phone = str(row.get("contact_number", "")).strip()
        email = str(row.get("email_id", "")).strip()
        address = str(row.get("address", "")).strip()

        required_fields = [hospital, specialization, district, phone, email, address]
        # Skip even if one of the important field is  empty...
        if any(v in ["No Name", ""] for v in required_fields):
            skipped_rows += 1
            continue
            ##Remove extra line issue ... Eg: abc123@
            ##                               gmail.com is converted to abc123@gmail.com
        hospital = hospital.replace("\n", " ").strip()
        specialization = specialization.replace("\n", " ").strip()
        district = district.replace("\n", " ").strip()
        phone = phone.replace("\n", " ").strip()
        email = email.replace("\n", "").replace(" ", "").strip()  # remove newlines & extra spaces
        address = " ".join(address.split()).strip()  # removes extra spaces, keeps single spaces
        text = f"""//Hospital Record//
Hospital Name: {hospital}
Specialization: {specialization}
District: {district}
Contact Number: {phone}
Email Id: {email}
Address: {address}
"""

        doc = Document(
            page_content=text,
            metadata={
                "hospital": hospital.lower(),
                "district": district.lower(),
                "specialization": specialization.lower()
            }
        )
        documents.append(doc)

    print(f"Converted {len(documents)} rows into documents for embeddings. Skipped {skipped_rows} empty rows.")

    print("Initializing embedding model...")
    embedding_model = get_embeddings()  # your HuggingFace embedding model

    print("Building FAISS vector index...")
    vectorstore = FAISS.from_documents(documents, embedding_model)

    print("Saving FAISS index locally...")
    vectorstore.save_local(INDEX_PATH)
    print("FAISS index built successfully!")

if __name__ == "__main__":
    Build_index()
