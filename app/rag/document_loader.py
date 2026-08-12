from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "documents"


def load_documents() -> list[dict]:
    """
    Load all TXT documents from the documents directory.

    Returns:
        A list containing document text and metadata.
    """

    documents = []

    for file_path in sorted(
        DOCUMENTS_DIR.glob("*.txt")
    ):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "source": file_path.name,
                "text": text,
            }
        )

    return documents