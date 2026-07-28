# Juris — AI Legal Contract Analyzer

> **Read Less. Understand More.**

Juris is an AI-powered legal contract analyzer that helps users understand employment contracts by combining **Retrieval-Augmented Generation (RAG)** with **Indian labour laws**. Instead of relying solely on a large language model, Juris retrieves relevant legal provisions from a structured knowledge base and uses them to generate grounded, clause-specific legal analysis.

---

## Features

* Upload employment contracts (PDF)
* Automatic clause extraction
* AI-powered clause-by-clause legal analysis
* Retrieval-Augmented Generation (RAG)
* Semantic search using vector embeddings
* References to relevant sections of Indian labour law
* Identification of risky, illegal, and missing clauses
* Plain-English explanations for complex legal language

---

## Architecture

```text
                   Employment Contract
                            │
                            ▼
                     PDF Processing
                            │
                            ▼
                    Clause Extraction
                            │
                            ▼
                 Embedding Generation
                            │
                            ▼
                Qdrant Vector Database
                            │
                 Relevant Legal Sections
                            │
                            ▼
                  OpenAI Large Language Model
                            │
                            ▼
                 Clause-by-Clause Analysis
                            │
                            ▼
                      Final Legal Report
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* OpenAI API
* LangChain

### AI & Retrieval

* Retrieval-Augmented Generation (RAG)
* OpenAI Embeddings
* Qdrant Vector Database
* Semantic Search

### Document Processing

* pdfplumber
* PyMuPDF

### Frontend

* React
* TypeScript

---

## Project Structure

```text
Legal_rag/
│
├── app/
│   ├── contract/        # Contract parsing & analysis
│   ├── kb/              # Knowledge base ingestion
│   ├── models/          # Data models
│   └── retrieval/       # RAG retrieval pipeline
│
├── Frontend/            # React application
├── data/                # Legal documents
├── uploads/             # Uploaded contracts
├── api.py               # FastAPI entry point
└── requirements.txt
```

---

## How It Works

### 1. Upload Contract

The user uploads an employment contract in PDF format.

### 2. Contract Parsing

The document is parsed and meaningful legal clauses are extracted.

### 3. Semantic Retrieval

Each clause is embedded and matched against a vector database containing Indian labour law provisions.

### 4. AI Analysis

The retrieved legal context and the contract clause are provided to the language model to produce grounded legal analysis.

### 5. Final Report

Juris returns:

* Clause summary
* Legal risk assessment
* Relevant legal references
* Missing clauses
* AI-generated recommendations

---

## 💡 Why I Chose Custom RAG?

Most RAG applications treat documents as plain text, splitting them into fixed-size chunks before storing them in a vector database. While this works well for general documents, it falls short for legal content where structure is as important as the text itself.
Legal documents follow a strict hierarchy:

Act
└── Chapter
    └── Section
        └── Clause

Breaking this hierarchy into arbitrary chunks can separate related provisions, lose legal context, and reduce retrieval quality.

My Approach

Instead of a generic RAG pipeline, Juris uses a custom retrieval architecture designed specifically for legal documents.

-> Hierarchical Document Modeling – Preserves the Act → Chapter → Section → Clause structure.
-> Semantic Chunking – Chunks are created at legal boundaries instead of fixed token sizes.
-> Rich Metadata Indexing – Every embedding retains legal context such as Act, Chapter, Section, and Clause.
-> Context-Aware Retrieval – Retrieves complete legal provisions instead of isolated text fragments.
-> Grounded AI Responses – The LLM reasons over retrieved legal context, producing more reliable and explainable analyses.
-> Why It Matters

By designing the retrieval pipeline around the structure of legal knowledge rather than relying on generic chunking strategies, Juris delivers:

Better retrieval relevance
Stronger context preservation
More accurate clause analysis
Explainable AI with legal references
A scalable foundation for future legal knowledge bases

The goal wasn't just to build another RAG application—it was to engineer a retrieval system that understands how legal documents are structured.
---

## Example Workflow

```text
Upload Contract
        │
        ▼
Extract Clauses
        │
        ▼
Generate Embeddings
        │
        ▼
Retrieve Relevant Law
        │
        ▼
LLM Analysis
        │
        ▼
Risk Assessment + Legal References
```

---

## Future Improvements

* Support for multiple contract types
* Multi-jurisdiction legal knowledge bases
* Citation highlighting inside uploaded PDFs
* Contract comparison
* Exportable analysis reports
* User authentication and analysis history

---

## Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd Legal_rag
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

macOS / Linux

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
```

### Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Run the backend

```bash
uvicorn api:app --reload
```

### Run the frontend

```bash
cd Frontend
npm install
npm run dev
```

---

## Key Concepts Demonstrated

* Retrieval-Augmented Generation (RAG)
* Vector Search
* Embedding-based Semantic Retrieval
* FastAPI Backend Development
* AI Application Architecture
* Document Parsing
* Prompt Engineering
* Backend API Design

---
