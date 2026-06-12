from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import QuestionRequest
from services.pdf_service import extract_text
from services.embedding_service import create_embeddings
from services.vector_store import VectorStore
from services.rag_service import get_answer

from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.file_utils import save_file, delete_file

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GLOBAL VECTOR STORE
vector_store = VectorStore()

# CHUNKER
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

# HOME
@app.get("/")
def home():
    return {"message": "RAG API Running 🚀"}

# UPLOAD PDF
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    content = await file.read()
    filename = save_file(content)

    text = extract_text(filename)
    chunks = splitter.split_text(text)

    embeddings = create_embeddings(chunks)

    vector_store.build_index(embeddings, chunks)

    delete_file(filename)

    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks)
    }

# ASK QUESTION
@app.post("/ask")
async def ask_question(request: QuestionRequest):

    if not vector_store.index:
        return {"error": "Upload PDF first"}

    query_embedding = create_embeddings([request.question])

    context_chunks = vector_store.search(query_embedding, top_k=3)

    context = "\n\n".join(context_chunks)

    answer = get_answer(context, request.question)

    return {
        "answer": answer,
        "context_used": context_chunks
    }