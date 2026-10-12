import chromadb

def create_collection():
    client = chromadb.PersistentClient(path="chromadb")
    collection = client.get_or_create_collection(name="company_policies")
    return collection

def store_chunks(chunks, collection):
    ids, documents, embeddings, metadatas = [],[],[],[]
    for index, chunk in enumerate(chunks):
        ids.append(f"chunk_{index}")
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])
        metadatas.append(chunk["metadata"])
        collection.add(ids=ids, documents = documents, embeddings = embeddings, metadatas = metadatas)

def query_collection(
    collection,
    query_embedding,
    n_results=3,
    metadata_filter = None
):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where = metadata_filter
    )

    return results