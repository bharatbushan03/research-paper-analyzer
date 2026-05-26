import faiss
import numpy as np
import os

def create_vector_store(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    embeddings = np.array(embeddings)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index

def save_index(index: faiss.IndexFlatL2, path: str):
    faiss.write_index(index, path)

def load_index(path: str) -> faiss.IndexFlatL2:
    return faiss.read_index(path)
