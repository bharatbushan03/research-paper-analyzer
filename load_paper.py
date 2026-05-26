from pypdf import PdfReader
from typing import Tuple, Dict, Any

def load_pdf(file_path: str) -> Tuple[str, Dict[str, Any]]:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Extract metadata
    info = reader.document_info
    metadata = {
        "Title": info.get("/Title", "Unknown Title"),
        "Author": info.get("/Author", "Unknown Author"),
        "Subject": info.get("/Subject", "N/A"),
        "Creator": info.get("/Creator", "N/A"),
    }

    return text, metadata
