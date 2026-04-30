# System Architecture

## Overview

The AI Compliance & Risk Intelligence Platform is designed as a governed AI workflow system for regulated environments.

The platform uses retrieval-augmented generation (RAG), structured AI outputs, human-in-the-loop review, and audit logging to support explainable and traceable compliance decision-making.

This is not designed to automate final compliance decisions. The system assists analysts by surfacing relevant policy context, generating risk analysis, and capturing human review decisions.

---

## Architecture Goals

- Ground AI outputs in approved source documents
- Reduce manual policy search and case review effort
- Preserve human oversight for final decisions
- Maintain complete auditability of AI-assisted workflows
- Support explainability, traceability, and governance
- Keep the MVP modular and easy to extend

---

## High-Level Architecture

```text
User
 |
 v
Streamlit UI / CLI
 |
 v
Workflow Layer
 |
 |----> Document Ingestion
 |        |
 |        v
 |     Chunking + Metadata
 |
 |----> Retrieval Layer
 |        |
 |        v
 |     Vector Store
 |
 |----> LLM Analysis Layer
 |        |
 |        v
 |     Structured AI Output
 |
 |----> Human Review Layer
 |        |
 |        v
 |     Final Decision
 |
 v
Audit Log / Evaluation Store
```

## Core Components

### 1. User Interface

The MVP will begin with either a command-line interface or a lightweight Streamlit app.

The interface should allow users to:
* Upload or load policy documents
* Ask policy questions
* Submit compliance case scenarios
* Review AI-generated recommendations
* Accept, edit, or override AI outputs
* View prior logged decisions

Streamlit is the preferred MVP interface because it provides a simple way to demonstrate the workflow visually without building a full frontend.

⸻

### 2. Document Ingestion Layer

The document ingestion layer converts source documents into searchable knowledge units.

Initial supported formats:
* Markdown
* Plain text
* Later: PDF

Ingestion steps:
1. Load documents
2. Extract text
3. Split documents into chunks
4. Attach metadata to each chunk
5. Store chunks for embedding and retrieval

Metadata should include:
* Document name
* Section title
* Chunk ID
* Source location
* Date loaded

This metadata is critical for citation, traceability, and audit review.

⸻

### 3. Embedding and Vector Store

The platform uses embeddings to represent document chunks as searchable vectors.

The vector store enables semantic retrieval of relevant policy sections based on user questions or case scenarios.

Planned MVP option:
* ChromaDB

The vector store should contain:
* Document chunk text
* Embedding vectors
* Source metadata
* Document identifiers

⸻

### 4. Retrieval Layer

The retrieval layer is responsible for finding relevant source context before the LLM generates a response.

Workflow:
1. User submits a question or case scenario
2. System embeds the input
3. System retrieves the most relevant document chunks
4. Retrieved chunks are passed to the LLM as grounded context
5. The LLM generates a response using only the provided context

Key design principle:

If the retrieved context does not support an answer, the system should say it does not have enough information.

⸻

### 5. LLM Analysis Layer

The LLM analysis layer generates structured outputs from user input and retrieved context.

The system should avoid free-form chatbot responses where possible. Outputs should follow a predictable structure.

Example output schema:

```JSON
{
  "summary": "",
  "risk_flags": [],
  "recommended_action": "",
  "supporting_sources": [],
  "confidence": "",
  "limitations": ""
}
```
The LLM is used for:
* Policy question answering
* Scenario summarization
* Risk flag identification
* Recommendation drafting
* Explanation generation

The LLM does not make final compliance decisions.

⸻

### 6. Human-in-the-Loop Review Layer

Human review is required before any recommendation becomes final.

Reviewer actions:
* Accept AI recommendation
* Edit AI recommendation
* Override AI recommendation
* Add reviewer notes
* Mark final decision

Captured review data:
* AI recommendation
* Human decision
* Reviewer notes
* Review timestamp
* Override reason, if applicable

This ensures that AI remains assistive rather than authoritative.

⸻

### 7. Audit Logging Layer

Every AI-assisted interaction should be logged.

The audit log should capture:
* Timestamp
* Workflow type
* User input
* Retrieved sources
* AI output
* Model used
* Human decision
* Reviewer notes
* Final outcome

MVP storage option:

* SQLite

Example audit log fields:

```text
audit_log
- id
- timestamp
- workflow_type
- user_input
- retrieved_sources
- ai_output
- ai_recommendation
- human_decision
- reviewer_notes
- model_name
```

Audit logging is a core feature, not an afterthought.

⸻

## Key Workflows

### Policy Q&A Workflow
```text
User asks policy question
 |
 v
Retrieve relevant policy chunks
 |
 v
Generate grounded answer
 |
 v
Display answer with sources
 |
 v
Log question, sources, and answer
```

### Case Analysis Workflow
```text
User submits case scenario
 |
 v
Retrieve relevant policy context
 |
 v
Generate structured risk analysis
 |
 v
Human reviews AI recommendation
 |
 v
Final decision is recorded
 |
 v
Full audit trail is saved
```
⸻

## Guardrails

### Source Grounding

The model should answer only from retrieved source material.

If the source material is insufficient, the response should state that clearly.

### Human Oversight

The system should not present AI recommendations as final decisions.

All outputs require human review.

### Structured Outputs

AI responses should be structured consistently to support review, logging, and evaluation.

### Traceability

Every recommendation should be traceable back to source documents, retrieved context, and reviewer action.

⸻

## MVP Tech Stack

| Layer            | Tool                          | Purpose |
|------------------|-------------------------------|---------|
| Language         | Python                        | Core application logic |
| UI               | Streamlit                     | Rapid prototyping interface |
| LLM              | OpenAI API / Anthropic API    | AI reasoning and generation |
| Vector Store     | ChromaDB                      | Semantic document retrieval |
| Audit Storage    | SQLite                        | Logging and traceability |
| Documents        | Markdown / TXT                | Initial knowledge base |
| Version Control  | GitHub                        | Code and documentation management |

## Design Tradeoffs

### Why RAG Instead of Fine-Tuning?

RAG is better suited for this MVP because:
* Source documents may change over time
* Compliance teams need citation-backed answers
* The system must support traceability
* Fine-tuning would not solve source attribution
* RAG is easier to iterate and evaluate

### Why Human Review?

Compliance decisions require accountability. The system is designed to assist analysts, not replace them.

Human review reduces risk and creates a defensible decision trail.

### Why SQLite for Audit Logging?

SQLite is simple, lightweight, and appropriate for an MVP. It allows structured logging without introducing unnecessary infrastructure complexity.

⸻

## Future Architecture Enhancements

Potential future improvements include:

* Role-based access controls
* Evaluation dashboard
* Batch document processing
* PDF ingestion
* Confidence scoring
* Model comparison
* Prompt/version tracking
* Red-team test suite
* Drift and quality monitoring
* Admin review dashboard

⸻

## Architecture Summary

This architecture demonstrates how AI can be integrated into regulated workflows responsibly.

The platform prioritizes:
* Grounded outputs
* Human oversight
* Structured recommendations
* Auditability
* Explainability
* Practical implementation

The goal is not to replace compliance professionals, but to help them make faster, more consistent, and more traceable decisions.
