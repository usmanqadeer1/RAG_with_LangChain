# ingest.py

import os
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(raw_docs)
    return chunks

def load_or_create_vectorstore(path):
    if os.path.exists("faiss_index"):
        print("✅ Loading existing FAISS index...")
        # return  Chroma(persist_directory="chroma_db", embedding_function=embedding_model)
        
        return FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

    
    else:
        print("📄 Index not found — creating...")
        
        chunks = load_documents(path)
        # vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory="chroma_db")
        # vectorstore.persist() 
        db = FAISS.from_documents(chunks, embedding_model)
        db.save_local("faiss_index")
        
        return db
