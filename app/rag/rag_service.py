from app.rag.search_service import (
    semantic_search,
)

from app.rag.llm_service import (
    generate_answer,
)


# ============================================================
# BUILD CONTEXT
# ============================================================

def build_context(
    results: list[dict],
) -> str:
    """
    Convert retrieved search results into
    context for the LLM.
    """

    context_parts = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        context_parts.append(
            f"""
SOURCE {index}
Document: {result['source']}
Chunk: {result['chunk_id']}
Similarity: {result['score']:.4f}

Content:
{result['text']}
"""
        )

    return "\n".join(
        context_parts
    )


# ============================================================
# RAG QUESTION ANSWERING
# ============================================================

def answer_question(
    question: str,
    top_k: int = 3,
) -> dict:
    """
    Retrieve relevant documents and generate
    a grounded answer using Groq.
    """

    results = semantic_search(
        question,
        top_k=top_k,
    )

    if not results:

        return {
            "question": question,
            "answer": (
                "I could not find relevant "
                "information in the supply-chain "
                "documents."
            ),
            "sources": [],
        }

    context = build_context(
        results
    )

    answer = generate_answer(
        question,
        context,
    )

    sources = [
        {
            "source": result["source"],
            "chunk_id": result["chunk_id"],
            "score": result["score"],
        }
        for result in results
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }