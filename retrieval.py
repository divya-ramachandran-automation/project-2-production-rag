from vector_store import query_collection
from reranker import rerank_chunks


def remove_duplicate_chunks(documents, metadatas, distances):
    seen = set()
    unique_chunks = []

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        normalized_text = " ".join(document.lower().split())

        if normalized_text not in seen:
            seen.add(normalized_text)

            unique_chunks.append({
                "text": document,
                "metadata": metadata,
                "distance": distance
            })

    return unique_chunks




def retrieve_relevant_chunks(
    collection,
    question,
    question_embedding,
    metadata_filter=None,
    n_results=5,
    distance_threshold=1.0
):
    try:
        results = query_collection(
            collection=collection,
            query_embedding=question_embedding,
            n_results=n_results,
            metadata_filter=metadata_filter
        )

        if not isinstance(results, dict):
            raise ValueError(
                "Retrieval returned an invalid result."
            )

        required_fields = [
            "documents",
            "metadatas",
            "distances"
        ]

        for field in required_fields:
            if field not in results:
                raise ValueError(
                    f"Retrieval result is missing the '{field}' field."
                )

        if not results["documents"] or not results["documents"][0]:
            return []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        filtered_chunks = []

        for document, metadata, distance in zip(
            documents, metadatas, distances
        ):
            if distance <= distance_threshold:
                filtered_chunks.append({
                    "text": document,
                    "metadata": metadata,
                    "distance": distance
                })

        unique_chunks = remove_duplicate_chunks(
            [chunk["text"] for chunk in filtered_chunks],
            [chunk["metadata"] for chunk in filtered_chunks],
            [chunk["distance"] for chunk in filtered_chunks]
        )

        reranked_chunks = rerank_chunks(
            question,
            chunks=unique_chunks
        )

        return reranked_chunks

    except Exception as error:
        print(f"Retrieval pipeline failed: {error}")
        raise

