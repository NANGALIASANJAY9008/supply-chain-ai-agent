from app.rag.search_service import (
    semantic_search,
)


def test_semantic_search():

    results = semantic_search(
        "When should inventory be reordered?",
        top_k=3,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) > 0

    assert len(results) <= 3

    for result in results:

        assert "score" in result
        assert "source" in result
        assert "chunk_id" in result
        assert "text" in result

        assert len(
            result["text"]
        ) > 0