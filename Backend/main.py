import os
import uuid
import numpy as np
import faiss

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

import google.generativeai as genai

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

stored_chunks = []
stored_index = None

class QuestionRequest(BaseModel):
    question: str

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def create_embeddings(chunks):
    return embedding_model.encode(chunks)


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    return index

# Routes
@app.get("/")
def home():
    return {"message": "RAG API is working 🚀"}

# UPLOAD PDF
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    global stored_chunks
    global stored_index

    # Safe filename
    filename = f"{uuid.uuid4()}.pdf"

    with open(filename, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text(filename)

    # Chunking
    chunks = chunk_text(text)

    # Embeddings
    embeddings = create_embeddings(chunks)

    # FAISS index
    index = create_faiss_index(embeddings)

    # Store globally
    stored_chunks = chunks
    stored_index = index

    # cleanup file (optional)
    os.remove(filename)

    return {
        "message": "PDF processed successfully",
        "total_chunks": len(chunks)
    }

# ASK QUESTION
@app.post("/ask")
async def ask_question(request: QuestionRequest):

    global stored_chunks
    global stored_index

    if stored_index is None:
        return {"error": "Upload a PDF first"}

    # Query embedding
    query_embedding = embedding_model.encode([request.question])

    # FAISS search
    distances, indices = stored_index.search(
        np.array(query_embedding).astype("float32"),
        3
    )

    # Build context
    context = ""
    for idx in indices[0]:
        context += stored_chunks[idx] + "\n\n"

    # Prompt for Gemini
    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.

Context:
{context}

Question:
{request.question}

If the answer is not in the context, say "Not found in document".
"""

    response = gemini_model.generate_content(prompt)

    return {
        "answer": response.text
    }