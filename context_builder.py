def build_context(reranked_chunks, max_chunks=3):
    if not reranked_chunks:
        return "No relevant information was found."

    selected_chunks = reranked_chunks[:max_chunks]

    context_parts = []

    for index, chunk in enumerate(selected_chunks, start=1):
        context_parts.append(
            f"[Source {index}]\n{chunk['text']}"
        )

    return "\n\n".join(context_parts)
    