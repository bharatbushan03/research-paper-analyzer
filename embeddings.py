from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        print("---- Loading Embedding Model (all-MiniLM-L6-v2) ----")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("---- Embeddings Model Loaded ----")
    return _model

def create_embeddings(chunks):
    model = get_model()
    # Extract text from Document objects
    texts = [doc.page_content for doc in chunks]
    embedded = model.encode(texts)
    return embedded