from typing import List, Dict

from openai import OpenAI
from dotenv import load_dotenv

from vector_store import search_policy_documents


load_dotenv()
client = OpenAI()

CHAT_MODEL = "gpt-4o-mini"


def format_context(matches: List[Dict]) -> str:
    context_blocks = []

    for index, match in enumerate(matches, start=1):
        source_label = f"Source {index}: {match['metadata']['document_name']} | {match['id']}"
        context_blocks.append(
            f"{source_label}\n{match['document']}"
        )

    return "\n\n".join(context_blocks)


def answer_policy_question(question: str) -> str:
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

Policy Context:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a cautious AI assistant for compliance policy review."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def main() -> None:
    question = input("Ask a policy question: ")
    answer = answer_policy_question(question)

    print("\nAnswer:")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()