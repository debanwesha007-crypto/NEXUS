from pathlib import Path
from typing import List
import hashlib
import json
import re
import sqlite3
import requests
import fitz
import numpy as np
import faiss
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
DB = DATA / "nexus.sqlite3"
INDEX = DATA / "vectors.faiss"
META = DATA / "metadata.json"
MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

app = FastAPI(title="NEXUS API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

embedder = SentenceTransformer(MODEL_NAME)
metadata = []
index = None

class AskRequest(BaseModel):
    question: str
    top_k: int = 5


def db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS documents (sha256 TEXT PRIMARY KEY, filename TEXT, pages INTEGER, status TEXT)")
    conn.commit()
    return conn


def load_state():
    global metadata, index
    if META.exists():
        metadata = json.loads(META.read_text(encoding="utf-8"))
    if INDEX.exists() and metadata:
        index = faiss.read_index(str(INDEX))


def save_state():
    if index is not None:
        faiss.write_index(index, str(INDEX))
    META.write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk(text: str, size=900, overlap=150):
    words = text.split()
    out = []
    step = max(1, size - overlap)
    for start in range(0, len(words), step):
        part = " ".join(words[start:start + size]).strip()
        if part:
            out.append(part)
        if start + size >= len(words):
            break
    return out


def answer_with_ollama(question: str, contexts: list[str]):
    context = "\n\n".join(contexts)
    prompt = f"""You are NEXUS, a document-grounded assistant. Answer only from the supplied context. If the context does not contain the answer, say: I could not find that in the uploaded documents. Do not invent facts.\n\nCONTEXT:\n{context}\n\nQUESTION: {question}\nANSWER:"""
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=45)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception:
        return None


load_state()

@app.get("/health")
def health():
    return {"status": "ok", "documents": len({m['sha256'] for m in metadata}), "chunks": len(metadata), "ollama": requests.get("http://localhost:11434/api/tags", timeout=2).ok if True else False}

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if len(files) > 50:
        raise HTTPException(400, "Maximum 50 PDFs per upload request")
    global index, metadata
    conn = db()
    added = []
    skipped = []
    errors = []
    texts, records = [], []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            errors.append({"filename": file.filename, "error": "Only PDF files are supported"})
            continue
        raw = await file.read()
        digest = hashlib.sha256(raw).hexdigest()
        if conn.execute("SELECT 1 FROM documents WHERE sha256=?", (digest,)).fetchone():
            skipped.append(file.filename)
            continue
        try:
            doc = fitz.open(stream=raw, filetype="pdf")
            if doc.page_count == 0:
                raise ValueError("PDF has no pages")
            page_count = doc.page_count
            for page_no, page in enumerate(doc, 1):
                text = clean_text(page.get_text())
                if not text:
                    continue
                for part in chunk(text):
                    texts.append(part)
                    records.append({"filename": file.filename, "page": page_no, "text": part, "sha256": digest})
            if not records or not any(r["sha256"] == digest for r in records):
                raise ValueError("No extractable text found; scanned PDF OCR is not enabled in this build")
            conn.execute("INSERT INTO documents VALUES (?, ?, ?, ?)", (digest, file.filename, page_count, "processed"))
            added.append(file.filename)
        except Exception as exc:
            errors.append({"filename": file.filename, "error": str(exc)})
    conn.commit()
    conn.close()
    if texts:
        vectors = embedder.encode(texts, normalize_embeddings=True, show_progress_bar=False).astype("float32")
        if index is None:
            index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        metadata.extend(records)
        save_state()
    return {"added": added, "skipped": skipped, "errors": errors, "chunks_added": len(texts)}

@app.get("/documents")
def documents():
    conn = db()
    rows = conn.execute("SELECT filename, pages, status FROM documents ORDER BY filename").fetchall()
    conn.close()
    return [{"filename": r[0], "pages": r[1], "status": r[2]} for r in rows]

@app.post("/ask")
def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    if index is None or not metadata:
        return {"answer": "Upload at least one PDF before asking a question.", "sources": []}
    query = embedder.encode([req.question], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(query, min(max(req.top_k, 1), len(metadata)))
    selected = []
    sources = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0:
            continue
        item = metadata[int(idx)]
        selected.append(item["text"])
        sources.append({"filename": item["filename"], "page": item["page"], "score": round(float(score), 4)})
    answer = answer_with_ollama(req.question, selected)
    if not answer:
        answer = "I found these relevant passages, but local generation is unavailable.\n\n" + "\n\n".join(selected[:3])
    return {"answer": answer, "sources": sources}
