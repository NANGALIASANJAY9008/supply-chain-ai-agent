from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents
from app.rag.embedding_service import generate_embeddings


def test_embedding_generation():

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    assert isinstance(
        embeddings,
        list,
    )

    assert len(embeddings) == len(
        texts
    )

    assert len(embeddings) > 0

    for embedding in embeddings:

        assert isinstance(
            embedding,
            list,
        )

        assert len(embedding) > 0