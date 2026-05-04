from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import shutil
import os
import traceback

from load_paper import load_pdf
from text_splitter import split_text
from embeddings import create_embeddings
from vector_store import create_vector_store
from search import search
from llm import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for the currently analyzed paper
current_paper = {
    "chunks": None,
    "index": None,
    "filename": None,
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    """Upload a PDF, extract text, and auto-generate analysis."""
    global current_paper

    try:
        print(f"\n{'='*50}")
        print(f"UPLOAD: '{file.filename}'")

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        print("[1/5] Saving file...")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("[2/5] Extracting text...")
        paper_text = load_pdf(file_path)

        if not paper_text:
            return JSONResponse(
                status_code=400,
                content={"error": "Could not extract text from this PDF. It may be a scanned image or password-protected."}
            )

        print("[3/5] Splitting text into chunks...")
        chunks = split_text(paper_text)

        print(f"[4/5] Creating embeddings for {len(chunks)} chunks...")
        embeddings = create_embeddings(chunks)
        index = create_vector_store(embeddings)

        # Store globally for follow-up questions
        current_paper["chunks"] = chunks
        current_paper["index"] = index
        current_paper["filename"] = file.filename

        # Step 5: Auto-generate analysis sections
        print("[5/5] Generating analysis...")
        analysis = {}

        prompts = {
            "summary": "Provide a comprehensive summary of this research paper in 3-4 sentences. What is the paper about?",
            "motivation": "What was the primary motivation or problem this research aimed to solve? Why is this work important?",
            "methodology": "What methodology or approach does this paper use? Describe the techniques, datasets, or frameworks used in detail.",
            "key_findings": "What are the key findings and results of this research paper? List the most important 3-4 points.",
            "limitations": "What are the limitations, constraints, or potential weaknesses mentioned in this research paper?",
            "conclusion": "What are the main conclusions and future directions suggested by this paper?"
        }

        for section, question in prompts.items():
            try:
                results = search(question, index, current_paper["chunks"])
                context = " ".join([doc.page_content for doc in results])
                answer = generate_answer(context, question)
                analysis[section] = answer
            except Exception as e:
                analysis[section] = f"Could not generate: {str(e)}"

        print("ANALYSIS COMPLETE\n")
        return JSONResponse(content={"analysis": analysis, "filename": file.filename})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ask")
async def ask_endpoint(data: QuestionRequest):
    """Answer follow-up questions about the analyzed paper."""
    global current_paper

    if current_paper["chunks"] is None:
        return JSONResponse(status_code=400, content={"error": "No paper uploaded yet."})

    try:
        print(f"QUESTION: {data.question}")
        results = search(data.question, current_paper["index"], current_paper["chunks"])
        context = " ".join([doc.page_content for doc in results])
        answer = generate_answer(context, data.question)
        return JSONResponse(content={"answer": answer})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join("frontend", "index.html"))