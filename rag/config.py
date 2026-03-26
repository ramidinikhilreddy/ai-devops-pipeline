from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_DIRS = [
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "backend",
    PROJECT_ROOT / "tests",
]

SUPPORTED_EXTENSIONS = {".md", ".py", ".txt", ".json"}

VECTOR_DIR = PROJECT_ROOT / "data" / "vector_store"
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = VECTOR_DIR / "faiss.index"
METADATA_FILE = VECTOR_DIR / "metadata.json"