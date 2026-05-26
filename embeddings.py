from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from logger import logger

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model (all-MiniLM-L6-v2)")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def create_embeddings(chunks: List[str]) -> np.ndarray:
    model = get_model()
    embeddings = model.encode(chunks)
    return embeddings
