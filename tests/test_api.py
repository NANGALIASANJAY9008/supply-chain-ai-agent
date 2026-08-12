from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


# ============================================================
# ROOT
# ============================================================

def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == (
        "Supply Chain Q&A Agent"
    )

    assert data["status"] == "running"


# ============================================================
# HEALTH
# ============================================================

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


# ============================================================
# ASK — SUCCESS
# ============================================================

@patch(
    "app.api.main.ask_supply_chain_agent"
)
def test_ask_success(
    mock_agent
):

    mock_agent.return_value = {
        "question": (
            "What is the current stock "
            "of P0084729?"
        ),
        "route": "SQL",
        "answer": (
            "The current stock is 962."
        ),
        "sql_data": {
            "type": "inventory"
        },
        "rag_data": None,
    }

    response = client.post(
        "/ask",
        json={
            "question": (
                "What is the current stock "
                "of P0084729?"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["route"] == "SQL"

    assert (
        data["answer"]
        == "The current stock is 962."
    )

    mock_agent.assert_called_once_with(
        "What is the current stock "
        "of P0084729?"
    )


# ============================================================
# ASK — EMPTY QUESTION
# ============================================================

def test_ask_empty_question():

    response = client.post(
        "/ask",
        json={
            "question": ""
        },
    )

    assert response.status_code == 422


# ============================================================
# ASK — WHITESPACE QUESTION
# ============================================================

def test_ask_whitespace_question():

    response = client.post(
        "/ask",
        json={
            "question": "   "
        },
    )

    assert response.status_code == 400


# ============================================================
# ASK — MISSING QUESTION
# ============================================================

def test_ask_missing_question():

    response = client.post(
        "/ask",
        json={}
    )

    assert response.status_code == 422


# ============================================================
# ASK — WRONG DATA TYPE
# ============================================================

def test_ask_invalid_type():

    response = client.post(
        "/ask",
        json={
            "question": 12345
        },
    )

    assert response.status_code == 422

# ============================================================
# CORS
# ============================================================

def test_cors_preflight():

    response = client.options(
        "/ask",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "access-control-allow-origin"
        ]
        == "http://localhost:5173"
    )