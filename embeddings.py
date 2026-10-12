import os
from config import API_KEY
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(API_KEY)
)

def create_embedding(text):
    response = client.embeddings.create(model = "text-embedding-3-small", input = text)
    return response.data[0].embedding

def create_embeddings(chunks):
    for chunk in chunks:
        embedding_response = create_embedding(chunk["text"])
        chunk["embedding"] = embedding_response
    return chunks
