from vector_store import search_policy_documents, format_context
from llm import get_structured_chat_completion
from audit import initialize_database, log_interaction
from pydantic import BaseModel


class CaseAnalysis(BaseModel):
    summary: str
    risk_flags: list[str]
    recommended_action: str
    confidence: str
    limitations: list[str]


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

Return a structured compliance analysis matching the required response schema.

Policy Context:
{context}

Case Scenario:
{case_text}
"""

    analysis = get_structured_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a cautious AI assistant for compliance case analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=CaseAnalysis,
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

    result = analyze_case_with_sources(case_text)["analysis"]

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
        ai_output=result.model_dump_json(),
        human_decision=human_decision,
        reviewer_notes=reviewer_notes,
    )
    print("\nAudit log saved.")


if __name__ == "__main__":
    main()