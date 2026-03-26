from pathlib import Path
from utils import chunk_text

DOCS_DIR = Path("data/project_docs")

def load_and_chunk_documents():
    chunked_docs = []

    for file_path in DOCS_DIR.glob("*"):
        if file_path.is_file():
            text = file_path.read_text(encoding="utf-8")
            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):
                chunked_docs.append({
                    "filename": file_path.name,
                    "chunk_id": i,
                    "text": chunk
                })

    return chunked_docs


if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    for c in chunks:
        print(c["filename"], c["chunk_id"], c["text"][:80])