from sentence_transformers import CrossEncoder

# load the pretrained ranking model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_chunks(question, chunks):
    if not chunks:
        return []
    pairs = [[question, chunk["text"]]
             for chunk in chunks]
    scores = reranker.predict(pairs)
    reranked_chunks = []
    for chunk, score in zip(chunks,scores):
        reranked_chunks.append({**chunk, "rerank_score": float(score)})
    reranked_chunks.sort(
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )

    return reranked_chunks
