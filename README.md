# NEXUS — Local RAG Chatbot
> Neural Extraction & Unified Search

A full-stack document intelligence and RAG application.

**🚀 [Live Demo](https://nexus-frontend-ejpo.onrender.com/)**
## Requirements
- Python 3.10+
- Node.js 18+
- Optional: Ollama for local answer generation

## Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal.

The app works in retrieval-only mode if Ollama is unavailable. For local generation:
```bash
ollama pull qwen2.5:3b
```
