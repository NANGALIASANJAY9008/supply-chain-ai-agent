import json
from pathlib import Path

from app.rag.rag_service import answer_question


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EVALUATION_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "rag_questions.json"
)


def load_questions():

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


questions = load_questions()

retrieval_correct = 0
total_questions = len(questions)


print("=" * 80)
print("SUPPLY CHAIN RAG EVALUATION")
print("=" * 80)


for number, item in enumerate(
    questions,
    start=1,
):

    question = item["question"]

    result = answer_question(
        question,
        top_k=3,
    )

    sources = [
        source["source"]
        for source in result["sources"]
    ]

    expected_source = (
        item["expected_source"]
    )

    correct = (
        expected_source
        in sources
    )

    if correct:
        retrieval_correct += 1

    print("\n")
    print("-" * 80)

    print(
        f"QUESTION {number}: "
        f"{question}"
    )

    print(
        f"Expected source: "
        f"{expected_source}"
    )

    print(
        f"Retrieved sources: "
        f"{sources}"
    )

    print(
        f"Retrieval: "
        f"{'PASS' if correct else 'FAIL'}"
    )

    print("\nANSWER:")

    print(
        result["answer"]
    )


retrieval_accuracy = (
    retrieval_correct
    / total_questions
) * 100


print("\n")
print("=" * 80)

print(
    f"Retrieval Accuracy: "
    f"{retrieval_accuracy:.2f}%"
)

print(
    f"Correct: "
    f"{retrieval_correct}/{total_questions}"
)

print("=" * 80)