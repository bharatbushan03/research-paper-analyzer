# Research Paper Analyzer (InsightPaper)

Upload a PDF research paper and get an instant AI-powered analysis. The app extracts text, builds embeddings, and generates summaries, key findings, methodology notes, and conclusions. You can also ask follow-up questions through a built-in chat UI.

## Features
- Upload a PDF and receive automated analysis sections
- Ask follow-up questions about the same paper
- Local model inference (no API keys required)
- Simple single-page frontend served by FastAPI

## Tech Stack
- **Backend:** FastAPI, Uvicorn
- **PDF parsing:** PyPDF
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector search:** FAISS
- **LLM:** Hugging Face Transformers (`google/flan-t5-small`)
- **Frontend:** HTML, CSS, JavaScript

## Getting Started

### Prerequisites
- Python 3.11+
- Internet access on first run to download model weights

### Installation
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run Locally
```bash
uvicorn app:app --reload
```

Open http://localhost:8000 in your browser.

## Usage
1. Upload a PDF from the landing page.
2. Wait while the analysis is generated.
3. Review summary, key findings, methodology, and conclusion.
4. Ask follow-up questions in the chat section.

> **Note:** The app works best with text-based PDFs. Scanned or image-only PDFs may fail to extract text.

## API Endpoints

### `POST /upload`
Uploads a PDF and generates the analysis.

- **Request:** `multipart/form-data` with `file`
- **Response:** `{ "analysis": { "summary": "...", "key_findings": "...", "methodology": "...", "conclusion": "..." }, "filename": "..." }`

### `POST /ask`
Ask a follow-up question about the most recently analyzed paper.

- **Request:** JSON body `{ "question": "..." }`
- **Response:** `{ "answer": "..." }`

### `GET /`
Serves the frontend UI.

## Project Structure
```
.
├── app.py                 # FastAPI app and API routes
├── embeddings.py          # Embedding model loader and encoder
├── load_paper.py          # PDF text extraction
├── llm.py                 # LLM prompt and generation logic
├── search.py              # Vector search helper
├── text_splitter.py       # Chunking logic
├── vector_store.py        # FAISS index creation
├── frontend/              # Static UI assets
│   ├── index.html
│   ├── script.js
│   └── style.css
├── requirements.txt
└── render.yaml            # Render deployment config
```

## Deployment
The repository includes a `render.yaml` with a default Render deployment setup:
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Optional Script Usage
`main.py` shows a simple script-based flow for running the pipeline locally. Update the PDF path before running it.
