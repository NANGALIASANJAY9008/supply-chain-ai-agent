from app.rag.embedding_service import (
    generate_embeddings,
)

from app.rag.vector_store import (
    load_faiss_index,
    load_metadata,
)


def semantic_search(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Search the FAISS vector store using
    semantic similarity.
    """

    index = load_faiss_index()

    metadata = load_metadata()

    query_embedding = generate_embeddings(
        [query]
    )

    query_vector = query_embedding[0]

    scores, indices = index.search(
        __import__("numpy").array(
            [query_vector],
            dtype="float32",
        ),
        top_k,
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0],
    ):

        if index_id < 0:
            continue

        chunk = metadata[index_id]

        results.append(
            {
                "score": float(score),
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
            }
        )

    return results