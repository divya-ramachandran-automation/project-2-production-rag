from retrieval import remove_duplicate_chunks


def test_remove_duplicate_chunks_removes_repeated_text():
    documents = [
        "Employees can take annual leave.",
        "Employees can take annual leave.",
        "Employees should inform their manager about sick leave."
    ]

    metadatas = [
        {"source": "leave_policy.txt"},
        {"source": "leave_policy.txt"},
        {"source": "hr_policy.txt"}
    ]

    distances = [0.2, 0.3, 0.4]

    unique_chunks = remove_duplicate_chunks(
        documents,
        metadatas,
        distances
    )

    assert len(unique_chunks) == 2
    assert unique_chunks[0]["text"] == "Employees can take annual leave."
    assert unique_chunks[1]["text"] == (
        "Employees should inform their manager about sick leave."
    )

def test_remove_duplicate_chunks_keeps_first_occurrence():
    documents = [
        "Employees can take annual leave.",
        "Employees can take annual leave."
    ]

    metadatas = [
        {"source": "leave_policy.txt"},
        {"source": "another_file.txt"}
    ]

    distances = [0.2, 0.8]

    unique_chunks = remove_duplicate_chunks(
        documents,
        metadatas,
        distances
    )

    assert len(unique_chunks) == 1
    assert unique_chunks[0]["metadata"]["source"] == "leave_policy.txt"
    assert unique_chunks[0]["distance"] == 0.2

def test_remove_duplicate_chunks_ignores_case_and_extra_spaces():
    documents = [
        "Employees can take annual leave.",
        "  EMPLOYEES   CAN take annual leave.  "
    ]

    metadatas = [
        {"source": "leave_policy.txt"},
        {"source": "another_file.txt"}
    ]

    distances = [0.2, 0.3]

    unique_chunks = remove_duplicate_chunks(
        documents,
        metadatas,
        distances
    )

    assert len(unique_chunks) == 1