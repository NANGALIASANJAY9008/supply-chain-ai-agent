from app.rag.rag_service import (
    answer_question,
)


questions = [
    "When should inventory be reordered?",
    "How are suppliers evaluated?",
    "What happens when a supplier delivers late?",
    "What products can be returned?",
    "What is the annual revenue of the company?",
]


for question in questions:

    print("\n")

    print("=" * 70)

    print(
        f"QUESTION: {question}"
    )

    print("=" * 70)

    result = answer_question(
        question,
        top_k=3,
    )

    print("\nANSWER:")

    print(
        result["answer"]
    )

    print("\nSOURCES:")

    for source in result["sources"]:

        print(
            f"- {source['source']} "
            f"(chunk {source['chunk_id']}, "
            f"score {source['score']:.4f})"
        )

    print("=" * 70)