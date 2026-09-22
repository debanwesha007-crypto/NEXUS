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
from sklearn.feature_extraction.text import HashingVectorizer


# ============================================================
# CONFIGURATION
# ============================================================

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

DB = DATA / "nexus.sqlite3"
INDEX = DATA / "vectors.faiss"
META = DATA / "metadata.json"

# Lightweight text-vectorization.
# This replaces SentenceTransformer to keep RAM usage low.
VECTOR_DIM = 1024

vectorizer = HashingVectorizer(
    n_features=VECTOR_DIM,
    alternate_sign=False,
    norm="l2"
)

# Ollama is local-only.
# It will not normally be available on Render.
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="NEXUS API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# GLOBAL STATE
# ============================================================

metadata = []
index = None


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


# ============================================================
# DATABASE
# ============================================================

def db():
    conn = sqlite3.connect(DB)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            sha256 TEXT PRIMARY KEY,
            filename TEXT,
            pages INTEGER,
            status TEXT
        )
        """
    )

    conn.commit()
    return conn


# ============================================================
# VECTOR / STATE MANAGEMENT
# ============================================================

def load_state():
    """
    Load the saved FAISS index and metadata.

    If an old index was created with a different vector size,
    it is ignored so the new application does not crash.
    """
    global metadata, index

    try:
        if META.exists():
            loaded_metadata = json.loads(
                META.read_text(encoding="utf-8")
            )

            if isinstance(loaded_metadata, list):
                metadata = loaded_metadata

        if INDEX.exists() and metadata:
            loaded_index = faiss.read_index(str(INDEX))

            # Make sure the old index matches our new vector size.
            if loaded_index.d == VECTOR_DIM:
                index = loaded_index
            else:
                print(
                    f"Ignoring old FAISS index with dimension "
                    f"{loaded_index.d}; expected {VECTOR_DIM}."
                )
                index = None
                metadata = []

    except Exception as exc:
        print(f"Could not load saved vector state: {exc}")
        index = None
        metadata = []


def save_state():
    if index is not None:
        faiss.write_index(index, str(INDEX))

    META.write_text(
        json.dumps(metadata, ensure_ascii=False),
        encoding="utf-8"
    )


def create_vectors(texts):
    """
    Convert text to lightweight vectors in batches.
    This avoids creating one huge temporary array in RAM.
    """
    if not texts:
        return np.empty((0, VECTOR_DIM), dtype="float32")

    batches = []

    batch_size = 32

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        vectors = (
            vectorizer
            .transform(batch)
            .toarray()
            .astype("float32")
        )

        batches.append(vectors)

    return np.vstack(batches)


# ============================================================
# TEXT PROCESSING
# ============================================================

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk(text: str, size=900, overlap=150):
    words = text.split()

    out = []

    step = max(1, size - overlap)

    for start in range(0, len(words), step):
        part = " ".join(
            words[start:start + size]
        ).strip()

        if part:
            out.append(part)

        if start + size >= len(words):
            break

    return out


# ============================================================
# OLLAMA
# ============================================================

def answer_with_ollama(question: str, contexts: list[str]):
    """
    Try local Ollama.

    On Render, Ollama normally won't be available, so this
    function safely returns None and the application falls
    back to returning relevant passages.
    """

    context = "\n\n".join(contexts)

    prompt = f"""
You are NEXUS, a document-grounded assistant.

Answer only from the supplied context.

If the context does not contain the answer, say:
I could not find that in the uploaded documents.

Do not invent facts.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json().get(
            "response",
            ""
        ).strip()

    except Exception:
        return None


# ============================================================
# LOAD EXISTING STATE
# ============================================================

load_state()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    unique_documents = {
        m["sha256"]
        for m in metadata
        if "sha256" in m
    }

    return {
        "status": "ok",
        "documents": len(unique_documents),
        "chunks": len(metadata),
        "ollama": False
    }


# ============================================================
# UPLOAD PDFS
# ============================================================

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if len(files) > 50:
        raise HTTPException(
            400,
            "Maximum 50 PDFs per upload request"
        )

    global index, metadata

    conn = db()

    added = []
    skipped = []
    errors = []

    try:

        for file in files:

            if not file.filename.lower().endswith(".pdf"):
                errors.append({
                    "filename": file.filename,
                    "error": "Only PDF files are supported"
                })
                continue

            try:
                raw = await file.read()

                digest = hashlib.sha256(raw).hexdigest()

                # Skip duplicate documents.
                if conn.execute(
                    "SELECT 1 FROM documents WHERE sha256=?",
                    (digest,)
                ).fetchone():

                    skipped.append(file.filename)
                    continue

                doc = fitz.open(
                    stream=raw,
                    filetype="pdf"
                )

                if doc.page_count == 0:
                    raise ValueError(
                        "PDF has no pages"
                    )

                page_count = doc.page_count

                file_texts = []
                file_records = []

                # Extract text.
                for page_no, page in enumerate(doc, 1):

                    text = clean_text(
                        page.get_text()
                    )

                    if not text:
                        continue

                    parts = chunk(text)

                    for part in parts:
                        file_texts.append(part)

                        file_records.append({
                            "filename": file.filename,
                            "page": page_no,
                            "text": part,
                            "sha256": digest
                        })

                doc.close()

                if not file_records:
                    raise ValueError(
                        "No extractable text found; "
                        "scanned PDF OCR is not enabled "
                        "in this build"
                    )

                # Create lightweight vectors.
                vectors = create_vectors(
                    file_texts
                )

                if vectors.shape[0] == 0:
                    raise ValueError(
                        "Could not create vectors"
                    )

                # Create FAISS index if necessary.
                if index is None:
                    index = faiss.IndexFlatIP(
                        VECTOR_DIM
                    )

                index.add(vectors)

                metadata.extend(
                    file_records
                )

                conn.execute(
                    """
                    INSERT INTO documents
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        digest,
                        file.filename,
                        page_count,
                        "processed"
                    )
                )

                conn.commit()

                added.append(file.filename)

                # Release temporary objects.
                del vectors
                del file_texts
                del file_records
                del raw

            except Exception as exc:

                errors.append({
                    "filename": file.filename,
                    "error": str(exc)
                })

        # Save the updated vector database.
        save_state()

    finally:
        conn.close()

    return {
        "added": added,
        "skipped": skipped,
        "errors": errors,
        "chunks_added": sum(
            1
            for m in metadata
            if m.get("filename") in added
        )
    }


# ============================================================
# LIST DOCUMENTS
# ============================================================

@app.get("/documents")
def documents():

    conn = db()

    rows = conn.execute(
        """
        SELECT filename, pages, status
        FROM documents
        ORDER BY filename
        """
    ).fetchall()

    conn.close()

    return [
        {
            "filename": row[0],
            "pages": row[1],
            "status": row[2]
        }
        for row in rows
    ]


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
def ask(req: AskRequest):

    if not req.question.strip():
        raise HTTPException(
            400,
            "Question cannot be empty"
        )

    if index is None or not metadata:
        return {
            "answer": (
                "Upload at least one PDF "
                "before asking a question."
            ),
            "sources": []
        }

    # Convert question to lightweight vector.
    query = (
        vectorizer
        .transform([req.question])
        .toarray()
        .astype("float32")
    )

    top_k = min(
        max(req.top_k, 1),
        len(metadata)
    )

    scores, ids = index.search(
        query,
        top_k
    )

    selected = []
    sources = []

    for score, idx in zip(
        scores[0],
        ids[0]
    ):

        if idx < 0:
            continue

        item = metadata[int(idx)]

        selected.append(
            item["text"]
        )

        sources.append({
            "filename": item["filename"],
            "page": item["page"],
            "score": round(
                float(score),
                4
            )
        })

    # Try Ollama.
    answer = answer_with_ollama(
        req.question,
        selected
    )

    # Render fallback.
    if not answer:
        answer = (
            "I found these relevant passages, "
            "but local generation is unavailable."
            "\n\n"
            + "\n\n".join(
                selected[:3]
            )
        )

    return {
        "answer": answer,
        "sources": sources
    }