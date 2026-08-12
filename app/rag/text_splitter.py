from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list[dict],
) -> list[dict]:
    """
    Split documents into smaller overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = []

    for document in documents:

        text_chunks = splitter.split_text(
            document["text"]
        )

        for index, chunk in enumerate(
            text_chunks
        ):

            chunks.append(
                {
                    "source": document["source"],
                    "chunk_id": index,
                    "text": chunk,
                }
            )

    return chunks