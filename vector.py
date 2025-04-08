from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os
import pandas as pd
import PyPDF2
from langchain_core.documents import Document

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            print(f"Page {page_num}: {page_text[:100]}")  
            text += page_text
        return text

def load_documents(file_path):
    ext = os.path.splitext(file_path)[-1].lower() 
    print(f"File Extension: {ext}")
    
    documents = []
    ids = []
    
    if ext == ".csv":
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            document = Document(
                page_content=row["Title"] + " " + row["Review"],
                metadata={"rating": row["Rating"], "date": row["Date"]}
            )
            ids.append(str(i))
            documents.append(document)
        return documents, ids
    
    elif ext == ".pdf":
        pdf_text = extract_text_from_pdf(file_path)
        document = Document(
            page_content=pdf_text,
            metadata={"source": file_path}
        )
        return [document], [str(0)] 
    
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or PDF.")

file_path = "Attention is all you need.pdf"  
print(f"File Path: {file_path}")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = f"./chroma_langchain_db_{os.path.basename(file_path).split('.')[0]}"


vector_store = Chroma(
    collection_name="content",
    persist_directory=db_location,
    embedding_function=embeddings,
)

try:
    documents, ids = load_documents(file_path)
    print(f"Loaded {len(documents)} documents.")
except ValueError as e:
    print(f"Error loading documents: {e}")
    
if documents:
    print(f"Adding {len(documents)} documents to vector store...")
    vector_store.add_documents(documents, ids=ids)
    print("Documents added to vector store.")

vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
print("Retriever set up.")
