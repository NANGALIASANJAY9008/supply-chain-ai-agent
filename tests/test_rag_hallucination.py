from app.rag.rag_service import answer_question


def test_unknown_question():

    question = (
        "What is the annual revenue "
        "of the company?"
    )

    result = answer_question(
        question,
        top_k=3,
    )

    answer = result["answer"].lower()

    refusal_phrases = [
        "do not provide",
        "does not provide",
        "not provide",
        "not available",
        "not mentioned",
        "not contain",
        "insufficient",
        "cannot determine",
        "don't have",
    ]

    assert any(
        phrase in answer
        for phrase in refusal_phrases
    )