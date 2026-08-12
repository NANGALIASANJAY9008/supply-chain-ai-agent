from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents


documents = load_documents()

chunks = split_documents(
    documents
)


print("=" * 70)
print("RAG DOCUMENT CHUNKING")
print("=" * 70)

print(
    f"Documents loaded: {len(documents)}"
)

print(
    f"Chunks created:   {len(chunks)}"
)

print("=" * 70)


for chunk in chunks[:5]:

    print(
        f"\nSource: {chunk['source']}"
    )

    print(
        f"Chunk ID: {chunk['chunk_id']}"
    )

    print(
        f"Text:\n{chunk['text'][:500]}"
    )

    print("-" * 70)