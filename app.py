
import os
import pandas as pd
from langchain_core.documents import Document
import PyPDF2
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def load_documents(file_path):
    ext = os.path.splitext(uploaded_file.name)[-1].lower() 
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
            metadata={"source": uploaded_file.name}
        )
        return [document], [str(0)] 
    
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or PDF.")

model = OllamaLLM(model="llama3.2")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
st.title("Document QA System")

uploaded_file = st.file_uploader("Upload a document", type=["csv", "pdf"])

if uploaded_file is not None:
    db_location = f"./chroma_langchain_db_{os.path.splitext(uploaded_file.name)[0]}"

    vector_store = Chroma(
        collection_name="content",
        persist_directory=db_location,
        embedding_function=embeddings,
    )




document_text = ""

if uploaded_file is not None:
    try:
        documents, ids = load_documents(uploaded_file)
        document_text = documents[0].page_content
        st.write("Document loaded successfully.")
        
        vector_store.add_documents(documents, ids=ids)
        st.success("Document added successfully to the vector store!")
    
    except ValueError as e:
        st.error(f"Error: {e}")


question = st.text_input("Ask a question about the document:")

if question:
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})  
    content = retriever.invoke(question)
    
    template = """
    You are an AI model tasked with answering questions based on the provided content.

Here is some relevant content:
{content}

Here is the question to answer:
{question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    result = chain.invoke({"content": content, "question": question})
    st.write(f"Answer: {result}")
