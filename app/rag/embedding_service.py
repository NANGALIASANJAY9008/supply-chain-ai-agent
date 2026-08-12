from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


# Load the model once when this module is imported.
model = SentenceTransformer(
    MODEL_NAME
)


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Convert text strings into embedding vectors.
    """

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()