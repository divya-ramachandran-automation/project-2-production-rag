def get_source_citations(retrieved_chunks):
    sources = []
    for chunk in retrieved_chunks:
        source = chunk["metadata"].get("source")
        if source and source not in sources:
            sources.append(source)
    return sources