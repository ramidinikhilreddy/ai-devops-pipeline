import os
import json
from pathlib import Path
import numpy as np
import faiss
from dotenv import load_dotenv
from openai import OpenAI

from ingest import load_and_chunk_documents

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INDEX_DIR = Path("data/faiss_index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = INDEX_DIR / "docs.index"
META_FILE = INDEX_DIR / "metadata.json"


def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def build_index():
    chunked_docs = load_and_chunk_documents()

    embeddings = []
    metadata = []

    for doc in chunked_docs:
        vector = get_embedding(doc["text"])
        embeddings.append(vector)
        metadata.append(doc)

    embeddings_np = np.array(embeddings).astype("float32")

    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    faiss.write_index(index, str(INDEX_FILE))

    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved {len(metadata)} chunks to FAISS index.")

    if __name__ == "__main__":
        build_index()