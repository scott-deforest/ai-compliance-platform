from pathlib import Path
from typing import List, Dict


POLICY_DIR = Path("data/policies")


def load_documents(policy_dir: Path = POLICY_DIR) -> List[Dict[str, str]]:
    """
    Load markdown and text policy documents from the policy directory.
    """
    documents = []

    if not policy_dir.exists():
        raise FileNotFoundError(f"Policy directory not found: {policy_dir}")

    for file_path in policy_dir.glob("*"):
        if file_path.suffix.lower() not in [".md", ".txt"]:
            continue

        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "document_name": file_path.name,
                "path": str(file_path),
                "text": text,
            }
        )

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks.
    This is intentionally simple for MVP purposes.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Convert loaded documents into chunks with metadata.
    """
    all_chunks = []

    for document in documents:
        chunks = chunk_text(document["text"])

        for index, chunk in enumerate(chunks, start=1):
            all_chunks.append(
                {
                    "chunk_id": f"{document['document_name']}_chunk_{index}",
                    "document_name": document["document_name"],
                    "source_path": document["path"],
                    "text": chunk,
                }
            )

    return all_chunks


def main() -> None:
    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Loaded {len(documents)} document(s)")
    print(f"Created {len(chunks)} chunk(s)")
    print()

    for chunk in chunks:
        print("=" * 80)
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Document: {chunk['document_name']}")
        print()
        print(chunk["text"])


if __name__ == "__main__":
    main()
