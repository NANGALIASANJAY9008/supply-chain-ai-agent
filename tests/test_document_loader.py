from app.rag.document_loader import (
    load_documents,
)


def test_document_loader():

    documents = load_documents()

    assert isinstance(
        documents,
        list,
    )

    assert len(documents) == 5

    for document in documents:

        assert "source" in document
        assert "text" in document

        assert len(
            document["text"]
        ) > 0