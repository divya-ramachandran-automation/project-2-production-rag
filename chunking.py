def chunk_document(text, metadata, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append({
            "text": text[start:end],
            "metadata": metadata
        })
        start += chunk_size - overlap
    return chunks

def chunk_documents(documents, chunk_size, overlap):
    all_chunks = []
    for document in documents:
        chunks = chunk_document(
            document["text"],
            document["metadata"],
            chunk_size,
            overlap
        )
        all_chunks.extend(chunks)
    return all_chunks