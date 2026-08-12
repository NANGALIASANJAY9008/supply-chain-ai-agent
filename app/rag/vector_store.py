from pathlib import Path
import json

import faiss
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

INDEX_PATH = (
    VECTORSTORE_DIR / "supply_chain.index"
)

METADATA_PATH = (
    VECTORSTORE_DIR / "metadata.json"
)


# ============================================================
# CREATE FAISS INDEX
# ============================================================

def create_faiss_index(
    embeddings: list[list[float]],
):
    """
    Create a FAISS index from embedding vectors.
    """

    vectors = np.array(
        embeddings,
        dtype="float32",
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(vectors)

    return index


# ============================================================
# SAVE FAISS INDEX
# ============================================================

def save_faiss_index(
    index,
) -> None:
    """
    Save FAISS index to disk.
    """

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss.write_index(
        index,
        str(INDEX_PATH),
    )


# ============================================================
# LOAD FAISS INDEX
# ============================================================

def load_faiss_index():
    """
    Load FAISS index from disk.
    """

    if not INDEX_PATH.exists():

        raise FileNotFoundError(
            f"FAISS index not found: "
            f"{INDEX_PATH}"
        )

    return faiss.read_index(
        str(INDEX_PATH)
    )


# ============================================================
# SAVE METADATA
# ============================================================

def save_metadata(
    chunks: list[dict],
) -> None:
    """
    Save chunk metadata corresponding to
    FAISS vector positions.
    """

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2,
        )


# ============================================================
# LOAD METADATA
# ============================================================

def load_metadata() -> list[dict]:
    """
    Load chunk metadata from disk.
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