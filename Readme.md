# 🧠 LLM Chatbot with RAG (Retrieval-Augmented Generation)

A full-stack, streaming AI chatbot application built with:

- 🔍 **LangChain** for RAG logic  
- 🦙 **LLaMA 3 via Ollama** as the local language model  
- ⚡ **FastAPI** for the backend with SSE streaming  
- 💬 **React** for the frontend chat interface  

---

## 🚀 Features

- 🔁 **Streaming responses** in real-time using Server-Sent Events (SSE)  
- 🧠 **Chat history aware** (context from previous turns is used)  
- 🎨 Clean and responsive frontend UI (React)  
- 🌐 CORS-enabled backend for local frontend/backend dev  

---

## 📁 Project Structure

rag-with-langchain/
│
├── backend/
│ ├── ingest.py # Loads and chunks documents, creates FAISS index
│ ├── rag_chain.py # Defines RAG chain using LangChain and Ollama
│ ├── app.py # FastAPI app exposing a /chat streaming endpoint
│ └── docs/ # Optional: Folder to store any local files
│
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── Chat.js # React chat component with streaming logic
│ │ └── index.js # App entry point
│ └── package.json # React app config
│
├── requirements.txt # Python dependencies
└── README.md 


---

## 🔧 Installation

### 1. Backend Setup

Make sure you have Python 3.10+ and [Ollama](https://ollama.com) installed.

```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload

cd rag-bot
npm install
npm start
