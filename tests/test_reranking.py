import reranker as reranker_module
from reranker import rerank_chunks


def test_rerank_chunks_sorts_by_score(monkeypatch):
    chunks = [
        {"text": "Annual leave is 24 days.", "metadata": {"source": "leave_policy.txt"}},
        {"text": "Remote work requires manager agreement.", "metadata": {"source": "remote_work_policy.txt"}}
    ]

    # Mock the model so the test doesn't run the real AI model
    monkeypatch.setattr(
        reranker_module.reranker,
        "predict",
        lambda pairs: [0.2, 0.9]
    )

    reranked_chunks = rerank_chunks(
        question="What is the remote work policy?",
        chunks=chunks
    )

    assert len(reranked_chunks) == 2
    assert reranked_chunks[0]["text"] == (
        "Remote work requires manager agreement."
    )
    assert reranked_chunks[0]["rerank_score"] == 0.9
    assert reranked_chunks[1]["rerank_score"] == 0.2

def test_rerank_chunks_returns_empty_list_for_no_chunks():
    result = rerank_chunks(
        question="What is the leave policy?",
        chunks=[]
    )

    assert result == []