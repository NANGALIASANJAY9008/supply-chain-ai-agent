import json
from pathlib import Path

import pytest

from app.rag.rag_service import answer_question


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EVALUATION_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "rag_questions.json"
)


def load_evaluation_questions():

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


QUESTIONS = load_evaluation_questions()


@pytest.mark.parametrize(
    "item",
    QUESTIONS,
)
def test_rag_answer_contains_expected_information(item):

    result = answer_question(
        item["question"],
        top_k=3,
    )

    answer = result["answer"].lower()

    assert len(answer) > 0

    for keyword in item["expected_keywords"]:

        assert keyword.lower() in answer