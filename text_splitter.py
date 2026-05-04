from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from load_paper import load_pdf

def split_text(docs):
    print("\n\nSplitting text....")
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )
        chunks = splitter.split_documents(docs)
        print("Documents successfully splitted")
        return chunks

    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    docs = load_pdf(r"C:\Users\dell\Downloads\How-to-Start-an-E-Commerce-Business-in-India-2026 (2).pdf")
    chunks = split_text(docs)
    if chunks == None:
        print("No chunks found")
    else :    
        print(f"No of chunks: {len(chunks)}")
        print(f"Type of data structure: {type(chunks)}")
