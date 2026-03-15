from load_paper import load_pdf
from text_splitter import split_text
from embeddings import create_embeddings
from vector_store import create_vector_store
from search import search
from llm import generate_answer

paper_text = load_pdf(r'C:\Users\dell\Downloads\attention-mechanism.pdf')

chunks = split_text(paper_text)

embeddings = create_embeddings(chunks)

index = create_vector_store(embeddings)

query = "What problem does the paper solve?"

results = search(query, index, chunks)

context = " ".join(results)

answer = generate_answer(context, query)

print("\nAnswer:\n")
print(answer)