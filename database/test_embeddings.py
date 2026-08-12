from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents
from app.rag.embedding_service import generate_embeddings


documents = load_documents()

chunks = split_documents(
    documents
)

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = generate_embeddings(
    texts
)


print("=" * 70)
print("EMBEDDING GENERATION")
print("=" * 70)

print(
    f"Documents: {len(documents)}"
)

print(
    f"Chunks:    {len(chunks)}"
)

print(
    f"Vectors:   {len(embeddings)}"
)

print(
    f"Dimensions per vector: "
    f"{len(embeddings[0])}"
)

print("=" * 70)

print("\nFirst vector preview:")

print(
    embeddings[0][:10]
)