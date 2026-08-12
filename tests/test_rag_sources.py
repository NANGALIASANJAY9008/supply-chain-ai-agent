from app.rag.rag_service import answer_question


def test_rag_returns_sources():

    result = answer_question(
        "When should inventory be reordered?",
        top_k=3,
    )

    assert "sources" in result

    assert isinstance(
        result["sources"],
        list,
    )

    assert len(
        result["sources"]
    ) > 0

    for source in result["sources"]:

        assert "source" in source
        assert "chunk_id" in source
        assert "score" in source