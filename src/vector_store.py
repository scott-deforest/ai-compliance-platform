from pathlib import Path
from typing import List, Dict

import chromadb
from dotenv import load_dotenv
from llm import get_embedding

from ingest import load_documents, create_chunks


CHROMA_PATH = Path("chroma_db")
COLLECTION_NAME = "policy_documents"
EMBEDDING_MODEL = "text-embedding-3-small"


load_dotenv()


def get_collection():
    """
    Create or load a persistent ChromaDB collection.
    """
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def index_policy_documents() -> None:
    """
    Load policy documents, chunk them, embed them, and store them in ChromaDB.
    """
    documents = load_documents()
    chunks = create_chunks(documents)
    collection = get_collection()

    for chunk in chunks:
        embedding = get_embedding(chunk["text"])

        collection.upsert(
            ids=[chunk["chunk_id"]],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[
    {
             "document_name": chunk["document_name"],
             "source_path": chunk["source_path"],
             "relative_path": chunk["relative_path"],
             "section": chunk["section"],
             "file_type": chunk["file_type"],
    }
],
        )

    print(f"Indexed {len(chunks)} chunk(s) into ChromaDB.")


def search_policy_documents(query: str, n_results: int = 3) -> List[Dict]:
    """
    Search ChromaDB for policy chunks relevant to the query.
    """
    collection = get_collection()
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    matches = []

    for i in range(len(results["ids"][0])):
        matches.append(
            {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return matches


def main() -> None:
    index_policy_documents()

    print()
    query = input("Ask a policy question: ")
    results = search_policy_documents(query)

    print("\nTop matches:")
    for match in results:
        print("=" * 80)
        print(f"Chunk ID: {match['id']}")
        print(f"Document: {match['metadata']['document_name']}")
        print(f"Distance: {match['distance']}")
        print()
        print(match["document"])


if __name__ == "__main__":
    main()