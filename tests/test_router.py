from app.agents.router import route_question


def test_sql_route():

    result = route_question(
        "What is the current stock of P0084729?"
    )

    assert result["route"] == "SQL"


def test_rag_route():

    result = route_question(
        "What is the inventory reorder policy?"
    )

    assert result["route"] == "RAG"


def test_both_route():

    result = route_question(
        "P0084729 is low in stock. "
        "What does the inventory policy recommend?"
    )

    assert result["route"] == "BOTH"