import os
from pathlib import Path

def get_metadata(file_name):
    if file_name == "benefits_policy.txt":
        return {
            "category":"benefits",
            "department":"HR",
            "year":2026

        }
    if file_name == "leave_policy.txt":
            return {
                "category":"leave",
                "department":"HR",
                "year":2026
    
            }
    if file_name == "hr_policy.txt":
            return {
                "category":"hr",
                "department":"HR",
                "year":2026
    
            }
    if file_name == "remote_work_policy.txt":
            return {
                "category":"remote_work",
                "department":"HR",
                "year":2026
    
            }
    return {
                     "category":"unknown",
                         "department":"unknown",
                         "year":2026
    }

def load_documents(folder_path):
    if not Path(folder_path).is_dir():
        raise FileNotFoundError(
            f"Knowledge folder not found: {folder_path}"
        )
    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "r", encoding = 'utf-8') as file:
                    text = file.read()
            except (OSError, UnicodeError) as error:
                raise RuntimeError(f"could not read document '{file_path}': {error}") from error
            text = text.strip()
            if not text:
                print(f"Skipping empty document: {file_name}")
                continue
            metadata = get_metadata(file_name)
            document = {"text":text,
                        "metadata":{
                                "source":file_name,
                                "category":metadata["category"],
                                "department":metadata["department"],
                                "year":metadata["year"]
                        }
                        }
            documents.append(document)
    if not documents:
        raise ValueError(
            f"No .txt documents found in folder: {folder_path}"
        )
    return documents

def ingest_documents(folder_path):
     documents = load_documents(folder_path)
     return documents