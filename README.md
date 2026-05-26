---
title: Research Paper Analyzer
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: streamlit
app_file: app.py
pinned: false
---

# Research Paper Analyzer (InsightPaper)

Upload a PDF research paper and get an instant AI-powered analysis. The app extracts text, builds embeddings, and generates summaries, key findings, methodology notes, and conclusions. You can also ask follow-up questions through a built-in chat UI.

## Features
- **Automated Analysis**: Instant summary, key findings, methodology, and conclusions.
- **AI Chat**: Ask follow-up questions with **full source citations** (View Sources).
- **Smart Caching**: Processed papers are cached locally to avoid redundant computations.
- **Metadata Extraction**: Automatically extracts Title and Author from the PDF.
- **Local Inference**: No API keys required, runs on local models.
- **Professional UI**: Clean, modern interface built with Streamlit.

## Tech Stack
- **Frontend & Backend:** Streamlit
- **PDF parsing:** PyPDF
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector search:** FAISS
- **LLM:** Hugging Face Transformers (`google/flan-t5-small`)

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
streamlit run app.py
```

Open the URL provided by Streamlit in your browser.

## Usage
1. Upload a PDF from the sidebar.
2. Wait while the analysis is generated.
3. Review summary, key findings, methodology, and conclusion.
4. Ask follow-up questions in the chat section.

> **Note:** The app works best with text-based PDFs. Scanned or image-only PDFs may fail to extract text.

## Project Structure
```
.
├── app.py                 # Streamlit app with UI and pipeline integration
├── embeddings.py          # Embedding model loader and encoder
├── load_paper.py          # PDF text extraction
├── llm.py                 # LLM prompt and generation logic
├── search.py              # Vector search helper
├── text_splitter.py       # Chunking logic
├── vector_store.py        # FAISS index creation
├── requirements.txt
└── render.yaml            # Render deployment config
```

## Deployment

### Hugging Face Spaces (Recommended)
The easiest way to deploy this project is using Hugging Face Spaces with the Streamlit SDK:
1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces).
2. Select **Streamlit** as the SDK.
3. Connect your GitHub repository or upload the files.
4. The app will automatically run `app.py` using the dependencies listed in `requirements.txt`.

### Render
The repository includes a `render.yaml` with a default Render deployment setup:
- Build: `pip install -r requirements.txt`
- Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## Optional Script Usage
`main.py` shows a simple script-based flow for running the pipeline locally. Update the PDF path before running it.
