def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80):
    """
    Split text into overlapping chunks, preferring sentence or newline boundaries.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            last_newline = text.rfind("\n", start, end)
            last_period = text.rfind(".", start, end)

            best_break = max(last_newline, last_period)
            if best_break > start:
                end = best_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = max(end - overlap, start + 1)

    return chunks