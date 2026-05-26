from typing import List
import numpy as np
import faiss
from embeddings import get_model

def search(query: str, index: faiss.IndexFlatL2, chunks: List[str], k: int = 5) -> List[str]:
    model = get_model()
    query_embedding = model.encode([query])

    D, I = index.search(np.array(query_embedding), k)

    results = [chunks[i] for i in I[0]]

    return results
