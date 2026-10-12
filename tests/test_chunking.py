from chunking import chunk_document, chunk_documents


def test_chunk_document_creates_overlapping_chunks():
    # Arrange: create text long enough for multiple chunks
    text = "A" * 500
    metadata = {"source": "leave_policy.txt"}

    # Act: split into chunks of 300 characters with 50 overlap
    chunks = chunk_document(
        text=text,
        metadata=metadata,
        chunk_size=300,
        overlap=50
    )

    # Assert: two chunks are created
    assert len(chunks) == 2

    # Each chunk has the expected length
    assert len(chunks[0]["text"]) == 300
    assert len(chunks[1]["text"]) == 250

    # Verify the 50-character overlap
    assert chunks[0]["text"][-50:] == chunks[1]["text"][:50]

def test_chunk_document_preserves_metadata():
    text = "A" * 350
    metadata = {
        "source": "leave_policy.txt",
        "category": "leave",
        "department": "HR",
        "year": 2026
    }

    chunks = chunk_document(
        text=text,
        metadata=metadata,
        chunk_size=300,
        overlap=50
    )

    assert len(chunks) == 2
    assert chunks[0]["metadata"] == metadata
    assert chunks[1]["metadata"] == metadata

def test_chunk_documents_processes_multiple_documents():
    documents = [
        {
            "text": "A" * 350,
            "metadata": {"source": "leave_policy.txt"}
        },
        {
            "text": "B" * 200,
            "metadata": {"source": "hr_policy.txt"}
        }
    ]

    chunks = chunk_documents(
        documents,
        chunk_size=300,
        overlap=50
    )

    # First document produces 2 chunks; second produces 1
    assert len(chunks) == 3

    # Check that chunks retain their original sources
    assert chunks[0]["metadata"]["source"] == "leave_policy.txt"
    assert chunks[1]["metadata"]["source"] == "leave_policy.txt"
    assert chunks[2]["metadata"]["source"] == "hr_policy.txt"