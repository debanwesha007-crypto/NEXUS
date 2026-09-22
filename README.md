# 🚀 NEXUS — Neural Extraction & Unified Search

<p align="center">

### 🧠 Document Intelligence • Retrieval-Augmented Generation • Full-Stack AI

A full-stack document intelligence and RAG application that allows users to upload multiple PDF documents, index their contents, search across them, and ask natural-language questions.

<br>

**🌐 [LIVE DEMO — OPEN NEXUS](https://nexus-frontend-ejpo.onrender.com/)**

<br><br>

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://nexus-frontend-ejpo.onrender.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue?style=for-the-badge)](https://react.dev/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge)](https://fastapi.tiangolo.com/)
[![Deployment](https://img.shields.io/badge/Deployment-Render-46E3B7?style=for-the-badge)](https://render.com/)

</p>

---

# 📌 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [How NEXUS Works](#-how-nexus-works)
- [System Architecture](#-system-architecture)
- [Application Flow](#-application-flow)
- [RAG Pipeline](#-rag-pipeline)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Frontend](#-frontend)
- [Backend](#-backend)
- [API Endpoints](#-api-endpoints)
- [Database & Storage](#-database--storage)
- [Vector Search](#-vector-search)
- [Optional Local LLM](#-optional-local-llm)
- [Local Installation](#-local-installation)
- [Backend Setup](#-backend-setup)
- [Frontend Setup](#-frontend-setup)
- [Running the Application](#-running-the-application)
- [Deployment](#-deployment)
- [Frontend–Backend Connection](#-frontendbackend-connection)
- [Example Workflow](#-example-workflow)
- [Use Cases](#-use-cases)
- [Project Highlights](#-project-highlights)
- [Future Improvements](#-future-improvements)
- [Author](#-author)
- [License](#-license)

---

# 🧠 Overview

**NEXUS — Neural Extraction & Unified Search** is a full-stack document intelligence application built around a **Retrieval-Augmented Generation (RAG)** workflow.

The application allows users to:

1. Upload multiple PDF documents.
2. Extract text from those documents.
3. Convert document content into searchable vector representations.
4. Build a searchable document index.
5. Ask natural-language questions.
6. Retrieve relevant document passages.
7. Display answers together with document and page-level source information.

NEXUS combines a **React + Vite frontend** with a **FastAPI backend**, vector-based retrieval, PDF processing, SQLite storage, and optional local LLM support.

---

# 🌐 Live Demo

## 🚀 [OPEN NEXUS — LIVE APPLICATION](https://nexus-frontend-ejpo.onrender.com/)

The deployed application provides the complete user-facing workflow:

```text
Open Website
     ↓
Upload Multiple PDFs
     ↓
Initialize Indexing
     ↓
Documents Become Searchable
     ↓
Ask a Question
     ↓
Retrieve Relevant Information
     ↓
Display Response + Sources
The system retrieves relevant content from the indexed documents and provides source information to help users understand where the retrieved information came from.
✨ Key Features
Feature	Description
📄 Multi-PDF Upload:     	Upload multiple PDF documents in a single batch
📖 PDF Text:        Extraction	Extract text from uploaded PDF files
🔎 Vector Search:  	Search document content using vector representations
💬 Natural-Language Queries:	Ask questions using normal language
📚 Source Information: 	Display document names and page numbers
⚡ FastAPI Backend: 	REST API for document processing and querying
🖥️ React Frontend:  	Interactive browser-based user interface
💾 SQLite:          	Local document metadata and application storage
🤖 Optional Ollama: 	Local LLM support
☁️ Render Deployment:	Publicly accessible frontend and backend
🔗 Frontend–Backend:  API	Frontend communicates with the deployed backend
🔄 How NEXUS Works

The complete application follows this workflow:
                    ┌──────────────────────┐
                    │      USER OPENS      │
                    │    NEXUS WEBSITE     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    UPLOAD PDFs       │
                    │   Multiple Files     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FASTAPI BACKEND    │
                    │    Receives Files    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   PDF TEXT           │
                    │   EXTRACTION         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ VECTOR              │
                    │ REPRESENTATION      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ SEARCHABLE          │
                    │ DOCUMENT INDEX      │
                    └──────────┬───────────┘
                               │
                               │
                       USER ASKS QUESTION
                               │
                               ▼
                    ┌──────────────────────┐
                    │   QUERY VECTOR      │
                    │    CREATION         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   VECTOR SEARCH     │
                    │   + RETRIEVAL       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ RELEVANT DOCUMENT   │
                    │     PASSAGES        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ RESPONSE + SOURCES  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FRONTEND UI      │
                    └──────────────────────┘
🏗️ System Architecture
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   NEXUS FRONTEND   │
                         │    React + Vite    │
                         └──────────┬──────────┘
                                    │
                              HTTP / REST
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   NEXUS BACKEND    │
                         │      FastAPI       │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
       ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
       │ PDF Processing │  │ Vector Search  │  │    SQLite      │
       │    PyMuPDF     │  │     FAISS      │  │    Storage     │
       └────────────────┘  │  Scikit-learn  │  └────────────────┘
                           └───────┬────────┘
                                   │
                                   ▼
                           ┌────────────────┐
                           │ Relevant       │
                           │ Passages       │
                           └───────┬────────┘
                                   │
                                   ▼
                           ┌────────────────┐
                           │ Optional LLM   │
                           │ Ollama / Qwen  │
                           └───────┬────────┘
                                   │
                                   ▼
                           ┌────────────────┐
                           │ Response +     │
                           │ Sources        │
                           └────────────────┘
The frontend communicates with the deployed backend through the configured API endpoint.

🧠 RAG Pipeline

NEXUS follows a retrieval-based document-questioning workflow.
                DOCUMENT INGESTION
                       │
                       ▼
                ┌──────────────┐
                │ Upload PDFs  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Extract Text │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Create       │
                │ Vectors      │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Store Index  │
                └──────────────┘


                QUERY PROCESSING
                       │
                       ▼
                ┌──────────────┐
                │ User Query   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Query Vector │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Vector Search│
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Top Relevant │
                │ Passages     │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Response +   │
                │ Sources      │
                └──────────────┘
🛠️ Technology Stack
Layer	                Technology	           Purpose
Frontend	            React	                 User interface
Frontend Build Tool	  Vite	                 Development and production builds
Programming         	JavaScript	           Frontend logic
Styling	              CSS	                   User interface styling
Backend	              Python	               Server-side application
API Framework	        FastAPI	               REST API
Server	              Uvicorn	               ASGI application server
PDF Processing	      PyMuPDF	               PDF text extraction
Vectorization	        Scikit-learn	         Text vectorization
Vector Search        	FAISS	                 Similarity search
Database	            SQLite	               Application/document metadata
Local LLM	            Ollama               	 Optional local generation
LLM	                  Qwen 2.5 3B	           Optional local answer generation
Deployment	          Render	               Cloud deployment

📂 Project Structure
NEXUS/
│
├── backend/
│   │
│   ├── app.py
│   │   ├── FastAPI application
│   │   ├── PDF processing
│   │   ├── Document indexing
│   │   ├── Vector search
│   │   └── Query processing
│   │
│   ├── requirements.txt
│   │
│   └── runtime.txt
│
├── frontend/
│   │
│   ├── src/
│   │   │
│   │   ├── main.jsx
│   │   │   └── React application
│   │   │
│   │   └── style.css
│   │       └── Application styling
│   │
│   ├── index.html
│   │
│   └── package.json
│
└── README.md
🎨 Frontend

The frontend is built using:
React
  +
Vite
  +
JavaScript
  +
CSS
The main frontend responsibilities are:

Responsibility	                       Description
File Selection	                       Select multiple PDF files
File Management                        Add/remove selected files
Upload	                               Send PDFs to backend
Query Input	                           Accept natural-language questions
API Communication	                     Communicate with FastAPI
Response Display	                     Display retrieved responses
Source Display	                       Display document/page information
Status Feedback                        Display indexing and query status
⚙️ Backend

The backend is built using FastAPI.

Its primary responsibilities include:

Responsibility	            Technology
REST API	                  FastAPI
PDF Processing	            PyMuPDF
Text Processing	            Scikit-learn
Vector Search	              FAISS
Metadata Storage	          SQLite
Optional Generation       	Ollama
Application Server	       Uvicorn

🔗 API Endpoints
Endpoint	    Method	            Purpose
/health	      GET	                Check backend health and status
/upload	      POST	              Upload and index PDF documents
/documents	  GET	                Retrieve indexed document information
/ask	        POST	              Ask questions against the indexed knowledge base

/health

Checks whether the backend is running.

/upload

Uploads one or multiple PDF documents.

/documents

Returns information about indexed documents.

/ask

Accepts a natural-language question.
The backend searches the indexed documents and returns relevant information.

💾 Database & Storage

NEXUS uses SQLite for application and document metadata.

The backend also maintains the vector search index used for document retrieval.

Conceptually:
PDF
 │
 ├── Extracted Text
 │
 ├── Document Metadata
 │
 └── Vector Representation
          │
          ▼
     Search Index
🔎 Vector Search

NEXUS uses a vector-based retrieval pipeline.

The current implementation uses:
Scikit-learn
      │
      ▼
HashingVectorizer
      │
      ▼
Vector Representation
      │
      ▼
FAISS
      │
      ▼
Similarity Search
When a user asks a question:
Question
   ↓
Question Vector
   ↓
FAISS Search
   ↓
Relevant Document Vectors
   ↓
Relevant Passages
🤖 Optional Local LLM

NEXUS can optionally use Ollama for local answer generation.

The configured model can be pulled using:

ollama pull qwen2.5:3b

The local workflow becomes:

User Question
      ↓
Vector Search
      ↓
Relevant Context
      ↓
Ollama / Qwen
      ↓
Generated Response

If Ollama is unavailable, the application can operate in retrieval-only mode.
💻 Local Installation
Requirements
Requirement	Version
Python	3.10+
Node.js	18+
npm	Included with Node.js
Git	Recommended
Ollama	Optional
🔧 Backend Setup

Navigate to the backend:

cd backend

Create a Python virtual environment:

python -m venv .venv
Windows
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn app:app --reload --port 8000

Backend:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs
🎨 Frontend Setup

Open a second terminal.

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Open the Vite URL displayed in the terminal.

▶️ Running the Complete Application Locally

Two terminals are required.

Terminal 1 — Backend
cd backend
.venv\Scripts\activate
uvicorn app:app --reload --port 8000
Terminal 2 — Frontend
cd frontend
npm install
npm run dev

Then:

Browser
   ↓
Frontend
   ↓
Backend
   ↓
Document Processing / Retrieval
☁️ Deployment

NEXUS is deployed using Render.

The deployment consists of two services:

                    NEXUS
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   ┌──────────────┐       ┌──────────────┐
   │   Frontend   │       │   Backend    │
   │ React + Vite │──────▶│   FastAPI    │
   │    Render    │  API  │    Render    │
   └──────────────┘       └──────────────┘
🌐 Frontend Deployment

The frontend is deployed as a Render Static Site.

Typical configuration:

Setting	Value
Service Type	Static Site
Root Directory	frontend
Build Command	npm install && npm run build
Publish Directory	dist
Branch	main
🖥️ Backend Deployment

The backend is deployed as a Render Web Service.

Typical configuration:

Setting	Value
Service Type	Web Service
Root Directory	backend
Build Command	pip install -r requirements.txt
Start Command	uvicorn app:app --host 0.0.0.0 --port 10000
Python	3.11.11
🔗 Frontend ↔ Backend Connection

The frontend is configured to communicate with the deployed FastAPI backend through its API URL.

                    USER
                      │
                      ▼
             NEXUS FRONTEND
                      │
                      │ HTTPS API
                      ▼
             NEXUS BACKEND
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        PDFs       Retrieval    Database

The user only needs to open the public frontend URL.

🌐 Public NEXUS Website

https://nexus-frontend-ejpo.onrender.com/

The backend operates behind the application as the API layer.

🔄 Complete Application Flow
┌─────────────────────────┐
│       OPEN NEXUS        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    SELECT PDF FILES     │
│     Multiple Files      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   INITIALIZE INDEXING   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     FASTAPI BACKEND     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    EXTRACT PDF TEXT     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   CREATE VECTORS        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     BUILD INDEX         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    DOCUMENTS READY      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      ASK QUESTION       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     VECTOR SEARCH       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ RETRIEVE RELEVANT TEXT  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   RESPONSE + SOURCES    │
└─────────────────────────┘
📚 Example Query Flow

Suppose the user uploads:

research-paper.pdf
machine-learning-notes.pdf
project-report.pdf

Then asks:

"What are the main techniques discussed in the documents?"

NEXUS performs:

Question
   ↓
Vectorize Question
   ↓
Search Indexed Documents
   ↓
Find Relevant Passages
   ↓
Identify Source Documents
   ↓
Return Relevant Information
   ↓
Display Results
🎯 Use Cases

NEXUS can be useful for:

Use Case	Example
📚 Education	Search through lecture notes
📄 Research	Query research papers
📑 Reports	Find information in large reports
🏢 Business	Search internal documents
📖 Study	Ask questions about study material
🧑‍💻 Technical Docs	Search technical documentation
📂 Knowledge Bases	Build searchable PDF collections
📝 Project Documentation	Query project reports

📊 Project Highlights
Category	                 Implementation
Application Type	         Full-Stack AI / RAG Application
Frontend	                 React + Vite
Backend	                   FastAPI
Language	                 Python + JavaScript
PDF Processing	           PyMuPDF
Vectorization	             Scikit-learn HashingVectorizer
Vector Database/Search	   FAISS
Metadata Database	         SQLite
Optional LLM	             Ollama + Qwen 2.5 3B
Document Input	           Multiple PDFs
Search	                   Vector-based retrieval
API	                       REST
Frontend Hosting	         Render
Backend Hosting	           Render
Status	                   Deployed

🧪 Testing Checklist

The deployed NEXUS application has been tested for the following workflow:

☑ Frontend loads
☑ Backend is reachable
☑ Multiple PDFs can be selected
☑ Multiple PDFs can be uploaded
☑ Documents can be indexed
☑ Queries can be submitted
☑ Relevant information can be retrieved
☑ Sources can be displayed
☑ Frontend communicates with backend
☑ Deployed application is accessible through a public URL
🔮 Future Improvements

Possible future improvements include:

Improvement	                          Purpose
🔐 Authentication	                    Secure user accounts
👤 User Workspaces	                  Separate knowledge bases per user
📂 Collections	                      Organize documents into groups
🗑️ Document Management	              Delete and manage indexed files
🧠 Advanced Embeddings	              Improve semantic retrieval
💾 Cloud Vector Database	            Persistent scalable storage
🤖 Hosted LLM	                        Cloud-based response generation
📊 Analytics	                        Track document/query usage
🔗 Shareable Knowledge Bases	        Share document collections
📱 Mobile Optimization	              Improve mobile experience
⚡ Streaming Responses	              Display generated responses progressively
📸 Screenshots

Screenshots can be added here to showcase the application.

Recommended screenshots:

1. NEXUS Homepage
2. Multiple PDF Upload
3. Document Indexing
4. Query Interface
5. Response + Sources

Example:

![NEXUS Dashboard](screenshots/dashboard.png)
🏆 Project Skills Demonstrated

This project demonstrates practical experience with:

Python
   │
   ├── FastAPI
   ├── REST APIs
   ├── PDF Processing
   └── Vector Retrieval
          │
          ▼
      RAG Concepts
          │
          ├── Document Ingestion
          ├── Vectorization
          ├── Similarity Search
          └── Context Retrieval

JavaScript
   │
   ├── React
   ├── Vite
   ├── API Integration
   └── Frontend State Management

Deployment
   │
   └── Render
🌟 Why NEXUS?

NEXUS demonstrates how a document-based AI system can be built from the ground up by combining:

Frontend Development
        +
Backend Development
        +
Document Processing
        +
Vector Search
        +
RAG Concepts
        +
API Integration
        +
Cloud Deployment
        =
Complete AI Application

👩‍💻 Author
Anwesha Deb

Computer Science / Artificial Intelligence & Machine Learning Student

Areas of Interest
🤖 Artificial Intelligence
🧠 Machine Learning
✨ Generative AI
🔎 Retrieval-Augmented Generation
🤝 Agentic AI
🐍 Python
🌐 Web Development
⚙️ Backend Development
🔗 Project Links
🌐 Live Application

🚀 Launch NEXUS

💻 GitHub Repository

📦 View NEXUS on GitHub

⭐ Support

If you found this project interesting, consider giving the repository a ⭐.

📄 License

This project is intended for educational and development purposes.
