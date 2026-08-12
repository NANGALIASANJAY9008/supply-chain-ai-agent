from app.agents.agent import (
    ask_supply_chain_agent,
)


def test_sql_agent_route():

    result = ask_supply_chain_agent(
        "What is the current stock of P0084729?"
    )

    assert result["route"] == "SQL"

    assert result["sql_data"] is not None

    inventory = (
        result["sql_data"]["inventory"]
    )

    assert (
        inventory["current_stock"]
        == 962
    )

    assert (
        inventory["reserved_stock"]
        == 32
    )

    assert (
        inventory["available_stock"]
        == 930
    )

    assert (
        inventory["reorder_level"]
        == 314
    )

    assert len(
        result["answer"]
    ) > 0

    answer = result["answer"].lower()

    # Current stock question must mention 962.
    assert "962" in answer


def test_rag_agent_route():

    result = ask_supply_chain_agent(
        "What is the inventory reorder policy?"
    )

    assert result["route"] == "RAG"

    assert result["rag_data"] is not None

    assert len(
        result["answer"]
    ) > 0


def test_both_agent_route():

    result = ask_supply_chain_agent(
        "P0084729 is low in stock. "
        "What does the inventory policy recommend?"
    )

    assert result["route"] == "BOTH"

    assert result["sql_data"] is not None

    assert result["rag_data"] is not None

    assert len(
        result["answer"]
    ) > 0

def test_natural_language_inventory():

    result = ask_supply_chain_agent(
        "Do we have enough P0084729?"
    )

    assert result["route"] == "SQL"

    assert result["sql_data"] is not None

    inventory = (
        result["sql_data"]["inventory"]
    )

    assert (
        inventory["available_stock"]
        == 930
    )

    assert (
        inventory["reorder_level"]
        == 314
    )

    answer = result["answer"].lower()

    assert "930" in answer