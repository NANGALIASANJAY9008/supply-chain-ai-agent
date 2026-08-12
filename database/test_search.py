from app.rag.search_service import (
    semantic_search,
)


questions = [
    "When should inventory be reordered?",
    "How are suppliers evaluated?",
    "What happens when a supplier delivers late?",
    "What products can be returned?",
]


for question in questions:

    print("=" * 70)

    print(
        f"QUESTION: {question}"
    )

    print("=" * 70)

    results = semantic_search(
        question,
        top_k=2,
    )

    for result in results:

        print(
            f"\nScore: {result['score']:.4f}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Chunk: {result['chunk_id']}"
        )

        print(
            f"Text:\n{result['text']}"
        )

        print("-" * 70)