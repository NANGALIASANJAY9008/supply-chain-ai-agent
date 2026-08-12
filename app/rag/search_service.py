import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

METADATA_PATH = (
    PROJECT_ROOT
    / "vectorstore"
    / "metadata.json"
)


# ============================================================
# TEXT TOKENIZATION
# ============================================================

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "who",
    "with",
}


def tokenize(text: str) -> set[str]:
    """
    Convert text into a lightweight set of
    meaningful lowercase words.
    """

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )

    return {
        word
        for word in words
        if word not in STOP_WORDS
        and len(word) > 2
    }


# ============================================================
# LOAD DOCUMENT METADATA
# ============================================================

def load_metadata() -> list[dict]:
    """
    Load the small document metadata file.
    """

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata file not found: "
            f"{METADATA_PATH}"
        )

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# LIGHTWEIGHT SEARCH
# ============================================================

def semantic_search(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Lightweight document retrieval.

    This intentionally avoids:
    - SentenceTransformer
    - PyTorch
    - FAISS
    - embedding models

    This keeps memory usage very low for
    Render's 512 MB Free instance.
    """

    metadata = load_metadata()

    if not metadata:
        return []

    query_words = tokenize(query)

    if not query_words:
        return []

    scored_results = []

    for chunk in metadata:

        text = chunk.get(
            "text",
            "",
        )

        chunk_words = tokenize(text)

        if not chunk_words:
            continue

        # Number of query words appearing
        # in the document chunk.
        overlap = query_words.intersection(
            chunk_words
        )

        if not overlap:
            continue

        # Basic relevance score.
        score = (
            len(overlap)
            / len(query_words)
        )

        # Small bonus when the exact query
        # phrase appears in the document.
        if query.lower() in text.lower():
            score += 0.25

        scored_results.append(
            {
                "score": min(score, 1.0),
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": text,
            }
        )

    # Highest relevance first.
    scored_results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return scored_results[:top_k]