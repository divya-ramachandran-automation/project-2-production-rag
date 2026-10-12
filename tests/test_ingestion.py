
from pathlib import Path
from ingestion import load_documents

def test_load_documents_reads_txt_files(tmp_path):
    # Arrange: create a temporary policy document
    policy_file = tmp_path / "leave_policy.txt"
    policy_file.write_text(
        "Employees can carry forward up to 10 vacation days.",
        encoding="utf-8"
    )

    # Act: load the document
    documents = load_documents(str(tmp_path))

    # Assert: verify the result
    assert len(documents) == 1
    assert documents[0]["text"] == (
        "Employees can carry forward up to 10 vacation days."
    )
    assert documents[0]["metadata"]["source"] == "leave_policy.txt"
    assert documents[0]["metadata"]["category"] == "leave"

def test_load_documents_skips_empty_files(tmp_path):
    # Arrange: create one empty file and one valid file
    (tmp_path / "empty_policy.txt").write_text(
        "",
        encoding="utf-8"
    )
    (tmp_path / "leave_policy.txt").write_text(
        "Employees can take annual leave.",
        encoding="utf-8"
    )

    # Act: load documents from the temporary folder
    documents = load_documents(str(tmp_path))

    # Assert: only the valid document is loaded
    assert len(documents) == 1
    assert documents[0]["metadata"]["source"] == "leave_policy.txt"
