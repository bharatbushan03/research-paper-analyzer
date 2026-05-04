import numpy as np
from embeddings import get_model

def search(query, index, chunks, k = 5):
    model = get_model()
    print(f"---- Searching for {query} ----")
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    # Filter out invalid indices (like -1) and ensure they are within bounds
    valid_indices = [i for i in I[0] if 0 <= i < len(chunks)]
    results = [chunks[i] for i in valid_indices]
    return results