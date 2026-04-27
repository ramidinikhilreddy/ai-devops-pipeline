import json

import faiss
import numpy as np

from rag.chunker import chunk_text
from rag.config import INDEX_FILE, METADATA_FILE
from rag.embedder import get_embedding
from rag.ingest import load_project_files


def load_and_chunk_project_files():
    """
    Load and chunk all supported project files.
    """
    raw_docs = load_project_files()
    chunked_docs = []

    for doc in raw_docs:
        chunks = chunk_text(doc["content"])

        for idx, chunk in enumerate(chunks):
            chunked_docs.append(
                {
                    "path": doc["path"],
                    "filename": doc["filename"],
                    "chunk_id": idx,
                    "text": chunk,
                }
            )

    return chunked_docs


def build_index():
    """
    Build and save the FAISS vector index and metadata.
    """
    chunked_docs = load_and_chunk_project_files()

    if not chunked_docs:
        raise ValueError("No documents found to index.")

    embeddings = []
    metadata = []

    for doc in chunked_docs:
        vector = get_embedding(doc["text"])
        embeddings.append(vector)
        metadata.append(doc)

    embeddings_np = np.array(embeddings, dtype="float32")
    dimension = embeddings_np.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    faiss.write_index(index, str(INDEX_FILE))

    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    print(f"Indexed {len(metadata)} chunks successfully.")


def load_index():
    """
    Load the FAISS index and metadata from disk.
    """
    index = faiss.read_index(str(INDEX_FILE))

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return index, metadata


def retrieve_context(ticket_text: str, top_k: int = 5):
    """
    Retrieve the most relevant chunks for a given ticket.
    """
    index, metadata = load_index()

    query_vector = get_embedding(ticket_text)
    query_np = np.array([query_vector], dtype="float32")

    distances, indices = index.search(query_np, top_k)

    results = []
    for idx in indices[0]:
        if idx != -1:
            results.append(metadata[idx])

    return results


if __name__ == "__main__":
    build_index()

    sample_ticket = """
    Build a user registration API with email validation,
    password hashing, duplicate email checks,
    and pytest-based test coverage.
    """

    retrieved = retrieve_context(sample_ticket, top_k=5)

    print("\nRetrieved Context:\n")
    for item in retrieved:
        print(f"File: {item['filename']} | Chunk: {item['chunk_id']}")
        print(item["text"])
        print("-" * 60)