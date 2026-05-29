from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader


POLICY_DIR = Path("data/policies")


def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text from a PDF file.
    """
    reader = PdfReader(str(file_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        if page_text.strip():
            pages.append(f"\n\n--- Page {page_number} ---\n\n{page_text}")

    return "\n".join(pages)


def load_documents(policy_dir: Path = POLICY_DIR) -> List[Dict[str, str]]:
    """
    Recursively load markdown, text, and PDF policy documents.
    """
    documents = []

    if not policy_dir.exists():
        raise FileNotFoundError(f"Policy directory not found: {policy_dir}")

    for file_path in policy_dir.rglob("*"):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        if suffix not in [".md", ".txt", ".pdf"]:
            continue

        if suffix == ".pdf":
            text = extract_text_from_pdf(file_path)
        else:
            text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            continue

        relative_path = file_path.relative_to(policy_dir)
        section = relative_path.parent.as_posix()

        documents.append(
            {
                "document_name": file_path.name,
                "path": str(file_path),
                "relative_path": str(relative_path),
                "section": section,
                "file_type": suffix.replace(".", ""),
                "text": text,
            }
        )

    return documents


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.
    Larger chunks work better for regulatory documents than the initial MVP size.
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

        safe_doc_name = document["relative_path"].replace("/", "_").replace(" ", "_")

        for index, chunk in enumerate(chunks, start=1):
            all_chunks.append(
                {
                    "chunk_id": f"{safe_doc_name}_chunk_{index}",
                    "document_name": document["document_name"],
                    "source_path": document["path"],
                    "relative_path": document["relative_path"],
                    "section": document["section"],
                    "file_type": document["file_type"],
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

    for document in documents:
        print("=" * 80)
        print(f"Document: {document['document_name']}")
        print(f"Section: {document['section']}")
        print(f"Type: {document['file_type']}")
        print(f"Path: {document['relative_path']}")

    print()
    print("Sample chunk:")
    print("=" * 80)

    if chunks:
        print(f"Chunk ID: {chunks[0]['chunk_id']}")
        print(f"Document: {chunks[0]['document_name']}")
        print(f"Section: {chunks[0]['section']}")
        print()
        print(chunks[0]["text"][:1500])


if __name__ == "__main__":
    main()