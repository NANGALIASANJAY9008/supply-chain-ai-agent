import pytest
import groq

from unittest.mock import patch

from app.agents.agent import (
    generate_final_answer,
)

from app.agents.errors import (
    LLMServiceError,
)

from app.agents.agent import (
    validate_question,
)

from app.agents.errors import (
    InvalidQuestionError,
)


def test_empty_question():

    with pytest.raises(
        InvalidQuestionError
    ):

        validate_question(
            ""
        )


def test_whitespace_question():

    with pytest.raises(
        InvalidQuestionError
    ):

        validate_question(
            "   "
        )


def test_none_question():

    with pytest.raises(
        InvalidQuestionError
    ):

        validate_question(
            None
        )


def test_non_string_question():

    with pytest.raises(
        InvalidQuestionError
    ):

        validate_question(
            123
        )


def test_question_too_long():

    question = "a" * 2001

    with pytest.raises(
        InvalidQuestionError
    ):

        validate_question(
            question
        )


def test_valid_question():

    question = (
        "What is the current stock "
        "of P0084729?"
    )

    result = validate_question(
        question
    )

    assert result == question


def test_question_is_trimmed():

    result = validate_question(
        "  What is inventory?  "
    )

    assert result == (
        "What is inventory?"
    )

from app.agents.dynamic_sql import (
    execute_dynamic_query,
)

from app.agents.errors import (
    QueryExecutionError,
)


def test_dynamic_sql_invalid_plan():

    invalid_plan = {
        "operation": "INVALID",
        "table": "products",
        "field": "*",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        QueryExecutionError
    ):

        execute_dynamic_query(
            invalid_plan
        )

def test_dynamic_sql_invalid_table():

    invalid_plan = {
        "operation": "FILTER",
        "table": "secret_table",
        "field": "*",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        QueryExecutionError
    ):

        execute_dynamic_query(
            invalid_plan
        )

from unittest.mock import patch

from app.agents.agent import (
    generate_final_answer,
)

from app.agents.errors import (
    LLMServiceError,
)

def test_groq_rate_limit():

    with patch(
        "app.agents.agent.client.chat.completions.create"
    ) as mock_create:

        mock_create.side_effect = Exception(
            "rate limit exceeded"
        )

        with pytest.raises(
            LLMServiceError
        ):

            generate_final_answer(
                question="What is inventory?",
                sql_data={
                    "type": "inventory"
                },
            )


def test_groq_request_too_large():

    with patch(
        "app.agents.agent.client.chat.completions.create"
    ) as mock_create:

        mock_create.side_effect = Exception(
            "request too large"
        )

        with pytest.raises(
            LLMServiceError
        ):

            generate_final_answer(
                question=(
                    "Which products have "
                    "a unit price above 50000?"
                ),
                sql_data={
                    "type": "dynamic_sql"
                },
            )


def test_groq_generic_failure():

    with patch(
        "app.agents.agent.client.chat.completions.create"
    ) as mock_create:

        mock_create.side_effect = (
            Exception(
                "Groq unavailable"
            )
        )

        with pytest.raises(
            LLMServiceError
        ):

            generate_final_answer(
                question="What is inventory?",
                sql_data={
                    "type": "inventory"
                },
            )