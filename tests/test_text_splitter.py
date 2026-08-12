from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents


def test_text_splitter():

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    assert isinstance(
        chunks,
        list,
    )

    assert len(chunks) > len(documents)

    for chunk in chunks:

        assert "source" in chunk
        assert "chunk_id" in chunk
        assert "text" in chunk

        assert len(
            chunk["text"]
        ) > 0

def test_all_documents_are_chunked():

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    sources = {
        chunk["source"]
        for chunk in chunks
    }

    assert len(sources) == 5