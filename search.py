import numpy as np
from embeddings import get_model

def search(query, index, chunks, k = 5):
    model = get_model()
    query_embedding = model.encode([query])
    
    D, I = index.search(np.array(query_embedding), k)

    results = [chunks[i] for i in I[0]]

    return results
