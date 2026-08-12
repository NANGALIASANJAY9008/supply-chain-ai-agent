from app.rag.rag_service import (
    build_context,
)


def test_build_context():

    results = [
        {
            "score": 0.91,
            "source": "inventory_policy.txt",
            "chunk_id": 2,
            "text": (
                "Available Stock = "
                "Current Stock - Reserved Stock."
            ),
        },
        {
            "score": 0.85,
            "source": "inventory_policy.txt",
            "chunk_id": 3,
            "text": (
                "When available stock falls "
                "below the reorder level, "
                "replenishment should be considered."
            ),
        },
    ]

    context = build_context(
        results
    )

    assert isinstance(
        context,
        str,
    )

    assert (
        "inventory_policy.txt"
        in context
    )

    assert (
        "Available Stock"
        in context
    )

    assert (
        "replenishment"
        in context
    )