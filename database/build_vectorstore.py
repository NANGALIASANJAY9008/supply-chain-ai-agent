from app.rag.document_loader import (
    load_documents,
)

from app.rag.text_splitter import (
    split_documents,
)

from app.rag.embedding_service import (
    generate_embeddings,
)

from app.rag.vector_store import (
    create_faiss_index,
    save_faiss_index,
    save_metadata,
)


print("=" * 70)
print("BUILDING SUPPLY CHAIN VECTOR STORE")
print("=" * 70)


# ============================================================
# STEP 1 — LOAD DOCUMENTS
# ============================================================

documents = load_documents()

print(
    f"Documents loaded: {len(documents)}"
)


# ============================================================
# STEP 2 — SPLIT DOCUMENTS
# ============================================================

chunks = split_documents(
    documents
)

print(
    f"Chunks created:   {len(chunks)}"
)


# ============================================================
# STEP 3 — EXTRACT TEXT
# ============================================================

texts = [
    chunk["text"]
    for chunk in chunks
]


# ============================================================
# STEP 4 — CREATE EMBEDDINGS
# ============================================================

embeddings = generate_embeddings(
    texts
)

print(
    f"Embeddings created: {len(embeddings)}"
)


# ============================================================
# STEP 5 — CREATE FAISS INDEX
# ============================================================

index = create_faiss_index(
    embeddings
)

print(
    f"FAISS vectors: {index.ntotal}"
)


# ============================================================
# STEP 6 — SAVE INDEX
# ============================================================

save_faiss_index(
    index
)

print(
    "FAISS index saved successfully."
)


# ============================================================
# STEP 7 — SAVE METADATA
# ============================================================

save_metadata(
    chunks
)

print(
    "Metadata saved successfully."
)

print("=" * 70)