from typing import List, Dict

from vector_store import search_policy_documents
from llm import get_chat_completion
from audit import initialize_database, log_interaction


def format_context(matches: List[Dict]) -> str:
    context_blocks = []

    for index, match in enumerate(matches, start=1):
        source_label = f"Source {index}: {match['metadata']['document_name']} | {match['id']}"

        context_blocks.append(
            f"{source_label}\n{match['document']}"
        )

    return "\n\n".join(context_blocks)


def analyze_case(case_text: str) -> str:
    matches = search_policy_documents(case_text)
    context = format_context(matches)

    prompt = f"""
You are an AI compliance risk analysis assistant.

Analyze the provided compliance scenario using ONLY the supplied policy context.

Rules:
- Do not use outside knowledge
- Do not make final compliance decisions
- Clearly identify limitations
- Use cautious and explainable reasoning
- Cite supporting sources where appropriate

Return your response using the following structure:

Summary:
<brief summary>

Risk Flags:
- flag 1
- flag 2

Recommended Action:
<recommended next step>

Supporting Sources:
- Source X
- Source Y

Confidence:
<Low / Medium / High>

Limitations:
<what information may be missing>

Policy Context:
{context}

Case Scenario:
{case_text}
"""

    return get_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a cautious AI assistant for compliance case analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

def analyze_case_with_sources(case_text: str) -> dict:
    matches = search_policy_documents(case_text)
    context = format_context(matches)

    prompt = f"""
You are an AI compliance risk analysis assistant.

Analyze the provided compliance scenario using ONLY the supplied policy context.

Rules:
- Do not use outside knowledge
- Do not make final compliance decisions
- Clearly identify limitations
- Use cautious and explainable reasoning
- Cite supporting sources where appropriate
- Confidence should usually be Low or Medium unless the policy context directly and fully supports the recommendation.

Return your response using the following structure:

Summary:
<brief summary>

Risk Flags:
- flag 1
- flag 2

Recommended Action:
<recommended next step>

Supporting Sources:
- Source X
- Source Y

Confidence:
<Low / Medium / High>

Limitations:
<what information may be missing>

Policy Context:
{context}

Case Scenario:
{case_text}
"""

    analysis = get_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a cautious AI assistant for compliance case analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "analysis": analysis,
        "sources": matches,
    }

def main() -> None:
    initialize_database()

    print("Enter compliance case scenario:")
    print("-" * 80)

    case_text = input("\nScenario:\n")

    result = analyze_case(case_text)

    print("\nCase Analysis")
    print("=" * 80)
    print(result)

    print("\nHuman Review")
    print("=" * 80)

    human_decision = input(
        "Final Decision (Accept / Escalate / Reject / Needs More Review): "
    )

    reviewer_notes = input("Reviewer Notes: ")

    log_interaction(
        workflow_type="case_analysis",
        user_input=case_text,
        ai_output=result,
        human_decision=human_decision,
        reviewer_notes=reviewer_notes,
    )
    print("\nAudit log saved.")


if __name__ == "__main__":
    main()