# 📄 AI PDF Chat Assistant (RAG System)

An AI-powered **PDF Chat Assistant** built using **FastAPI, React, FAISS, and Google Gemini API**.

Users can upload PDF documents and interact with them using natural language queries.

The system uses **Retrieval-Augmented Generation (RAG)** to fetch relevant document context and generate accurate AI responses.

---

## 🧠 Tech Stack

### Backend
- FastAPI
- Python 3.10+
- Sentence Transformers
- FAISS (Vector Database)
- LangChain
- PyPDF
- Google Gemini API

### Frontend
- React 19
- Vite
- Axios
- CSS (Custom Styling)

### AI / LLM
- Gemini 2.5 Flash (Google GenAI SDK)

---

## ⚙️ System Architecture

PDF Upload → Text Extraction → Chunking → Embeddings → FAISS → Retrieval → Gemini → Answer