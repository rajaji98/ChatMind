import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "backend" / "data" / "messages.json"
EMBEDDING_DIR = BASE_DIR / "embeddings"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def build_context(messages, index, radius=2):
    start = max(0, index - radius)
    end = min(len(messages), index + radius + 1)

    parts = []

    for i in range(start, end):
        message = messages[i]

        parts.append(
            f"{message['sender']}: {message['text']}"
        )

    return " | ".join(parts)


def main():
    print("Loading chat dataset...")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)

    print(f"Messages found: {len(messages)}")

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Building conversation-aware text...")

    texts = []

    for i in range(len(messages)):
        context = build_context(messages, i)

        texts.append(context)

    print("Generating conversation-aware embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    EMBEDDING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = EMBEDDING_DIR / "messages.npy"

    np.save(
        output_file,
        embeddings
    )

    print()
    print("=" * 50)
    print("EMBEDDINGS GENERATED")
    print("=" * 50)
    print(f"Shape  : {embeddings.shape}")
    print(f"Output : {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()