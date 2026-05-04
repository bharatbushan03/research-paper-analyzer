from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    print("Loading PDF....")
    try:
        loader = PyPDFLoader(file_path, mode = 'page')
        docs = loader.load()
        print(f"No. of Pages: {len(docs)}")
        print(f"Type of data structure: {type(docs)}")
        print("Document successful loaded")
        return docs
        
    except Exception as e:
        print(f"Error: {e}")
    return None