from typing import List, Dict

from dotenv import load_dotenv

from vector_store import search_policy_documents
from llm import get_chat_completion
from audit import initialize_database, log_interaction


load_dotenv()


def format_context(matches: List[Dict]) -> str:
    context_blocks = []

    for index, match in enumerate(matches, start=1):
        source_label = f"Source {index}: {match['metadata']['document_name']} | {match['id']}"
        context_blocks.append(
            f"{source_label}\n{match['document']}"
        )

    return "\n\n".join(context_blocks)


def answer_policy_question_with_sources(question: str) -> dict:
    matches = search_policy_documents(question)
    context = format_context(matches)

    prompt = f"""
You are an AI compliance assistant.

Answer the user's question using only the provided policy context.

Rules:
- Do not use outside knowledge.
- If the context does not contain enough information, say so.
- Cite sources using the provided Source numbers.
- Clearly state any limitations.
- Do not make final compliance decisions.
- Confidence should usually be Low or Medium unless the policy context directly and fully supports the recommendation.

Policy Context:
{context}

User Question:
{question}
"""

    answer = get_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a cautious AI assistant for compliance policy review."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    initialize_database()
    log_interaction(
        workflow_type="policy_qa",
        user_input=question,
        ai_output=answer,
        human_decision="N/A",
        reviewer_notes="",
    )

    return {
        "answer": answer,
        "sources": matches,
    }


def main() -> None:
    question = input("Ask a policy question: ")
    result = answer_policy_question_with_sources(question)

    print("\nAnswer:")
    print("=" * 80)
    print(result["answer"])

    print("\nRetrieved Sources:")
    print("=" * 80)

    for index, source in enumerate(result["sources"], start=1):
        metadata = source["metadata"]
        print(f"Source {index}: {metadata.get('document_name', 'Unknown document')}")
        print(f"Section: {metadata.get('section', 'Unknown section')}")
        print(f"Chunk ID: {source['id']}")
        print("-" * 80)


if __name__ == "__main__":
    main()