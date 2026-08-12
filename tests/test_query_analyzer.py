import pytest

from app.agents.query_analyzer import (
    analyze_query,
)


@pytest.mark.parametrize(
    "question,expected_intent",
    [
        (
            "What is the current stock of P0084729?",
            "INVENTORY_LOOKUP",
        ),
        (
            "Do we have enough P0084729 available?",
            "INVENTORY_LOOKUP",
        ),
        (
            "How much inventory is available for P0084729?",
            "INVENTORY_LOOKUP",
        ),
        (
            "Tell me about supplier S003821.",
            "SUPPLIER_LOOKUP",
        ),
        (
            "Which suppliers are the most reliable?",
            "TOP_RELIABLE_SUPPLIERS",
        ),
        (
            "Which suppliers have the highest delays?",
            "SUPPLIER_RISK",
        ),
        (
            "Show me products that need replenishment.",
            "LOW_STOCK",
        ),
        (
            "What is order O000500001?",
            "ORDER_LOOKUP",
        ),
        (
            "Show orders for P0084729.",
            "PRODUCT_ORDERS",
        ),
        (
            "Show me pending orders.",
            "ACTIVE_ORDERS",
        ),
    ],
)
def test_query_intent(
    question,
    expected_intent,
):

    result = analyze_query(
        question
    )

    assert (
        result["intent"]
        == expected_intent
    )

def test_dynamic_filter_query():

    result = analyze_query(
        "Which products have a unit price above 50000?"
    )

    assert result["intent"] == "UNKNOWN"