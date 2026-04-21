from rag.config import SOURCE_DIRS, SUPPORTED_EXTENSIONS


def load_project_files():
    """
    Load supported files from the project knowledge base.
    """
    documents = []

    for base_dir in SOURCE_DIRS:
        if not base_dir.exists():
            continue

        for file_path in base_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in SUPPORTED_EXTENSIONS:
                try:
                    content = file_path.read_text(encoding="utf-8")
                    documents.append(
                        {
                            "path": str(file_path),
                            "filename": file_path.name,
                            "content": content,
                        }
                    )
                except Exception as exc:
                    print(f"Skipping {file_path}: {exc}")

    return documents


if __name__ == "__main__":
    docs = load_project_files()
    print(f"Loaded {len(docs)} files.")
    for doc in docs:
        print(doc["path"])