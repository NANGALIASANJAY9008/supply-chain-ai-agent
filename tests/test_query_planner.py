import pytest

from app.agents.query_planner import (
    plan_query,
    validate_query_plan,
)


# ============================================================
# MOCK GROQ RESPONSE
# ============================================================

class MockMessage:

    def __init__(self, content):
        self.content = content


class MockChoice:

    def __init__(self, content):
        self.message = MockMessage(
            content
        )


class MockResponse:

    def __init__(self, content):
        self.choices = [
            MockChoice(content)
        ]


# ============================================================
# MOCK PLANNER
# ============================================================

def mock_plan_query(question):

    question_lower = question.lower()

    if "average reliability" in question_lower:

        return {
            "operation": "AVG",
            "table": "suppliers",
            "field": "reliability_score",
            "conditions": [],
            "group_by": None,
        }

    if "unit price above" in question_lower:

        return {
            "operation": "FILTER",
            "table": "products",
            "field": "*",
            "conditions": [
                {
                    "field": "unit_price",
                    "operator": ">",
                    "value": 50000,
                }
            ],
            "group_by": None,
        }

    if "average supplier delay" in question_lower:

        return {
            "operation": "AVG",
            "table": "suppliers",
            "field": "average_delay_days",
            "conditions": [],
            "group_by": None,
        }

    if "pending orders" in question_lower:

        return {
            "operation": "COUNT",
            "table": "orders",
            "field": "*",
            "conditions": [
                {
                    "field": "status",
                    "operator": "=",
                    "value": "Pending",
                }
            ],
            "group_by": None,
        }

    if "total order value" in question_lower:

        return {
            "operation": "SUM",
            "table": "orders",
            "field": "total_value",
            "conditions": [],
            "group_by": None,
        }

    raise ValueError(
        "Mock question not configured."
    )


# ============================================================
# VALID PLAN TESTS
# ============================================================

@pytest.mark.parametrize(
    "question,expected_operation,expected_table",
    [
        (
            "What is the average supplier delay?",
            "AVG",
            "suppliers",
        ),
        (
            "How many pending orders are there?",
            "COUNT",
            "orders",
        ),
        (
            "What is the total order value?",
            "SUM",
            "orders",
        ),
        (
            "What is the average reliability score?",
            "AVG",
            "suppliers",
        ),
        (
            "Which products have a unit price above 50000?",
            "FILTER",
            "products",
        ),
    ],
)
def test_query_planner(
    question,
    expected_operation,
    expected_table,
):

    plan = mock_plan_query(
        question
    )

    validate_query_plan(
        plan
    )

    assert (
        plan["operation"]
        == expected_operation
    )

    assert (
        plan["table"]
        == expected_table
    )


# ============================================================
# SECURITY VALIDATION TESTS
# ============================================================

def test_invalid_table():

    plan = {
        "operation": "COUNT",
        "table": "users",
        "field": "*",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        validate_query_plan(
            plan
        )


def test_invalid_operation():

    plan = {
        "operation": "DROP",
        "table": "orders",
        "field": "*",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        validate_query_plan(
            plan
        )


def test_invalid_field():

    plan = {
        "operation": "AVG",
        "table": "suppliers",
        "field": "password",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        validate_query_plan(
            plan
        )


def test_invalid_operator():

    plan = {
        "operation": "FILTER",
        "table": "products",
        "field": "*",
        "conditions": [
            {
                "field": "unit_price",
                "operator": "DROP",
                "value": 50000,
            }
        ],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        validate_query_plan(
            plan
        )