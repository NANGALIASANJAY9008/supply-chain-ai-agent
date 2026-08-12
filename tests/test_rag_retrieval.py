import json
from pathlib import Path

import pytest

from app.rag.search_service import semantic_search


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
def test_rag_retrieval_sources(item):

    results = semantic_search(
        item["question"],
        top_k=3,
    )

    assert len(results) > 0

    sources = [
        result["source"]
        for result in results
    ]

    assert (
        item["expected_source"]
        in sources
    )