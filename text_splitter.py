from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str) -> List[str]:
    # Use a slightly smaller chunk size for better precision in RAG
    # and a modest overlap to maintain context between chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100,
        length_function = len,
        is_separator_between_paragraphs = False,
    )

    chunks = text_splitter.split_text(text)
    return chunks
