from sentence_transformers import SentenceTransformer
from logger import logger

_model = None

def get_model():
    global _model
    if _model is None:
        logger.info("Loading embedding model (all-MiniLM-L6-v2)")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def create_embeddings(chunks):
    model = get_model()
    embeddings = model.encode(chunks)
    return embeddings