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
