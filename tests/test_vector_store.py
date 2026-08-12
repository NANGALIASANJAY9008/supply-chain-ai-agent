from app.rag.vector_store import (
    load_faiss_index,
)


def test_faiss_index():

    index = load_faiss_index()

    assert index is not None

    assert index.ntotal == 11

    assert index.d == 384