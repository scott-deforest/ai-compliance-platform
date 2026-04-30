# MVP Scope

## Overview

This document defines the minimum viable product (MVP) scope for the AI Compliance & Risk Intelligence Platform.

The goal of the MVP is to demonstrate a realistic, end-to-end AI-assisted workflow for compliance decision-making, including:

- Document-based question answering (RAG)
- AI-assisted case analysis
- Human-in-the-loop review
- Audit logging and traceability

The MVP prioritizes **functionality, explainability, and governance** over UI polish or scale.

---

## MVP Goals

The MVP is designed to prove:

- AI can be integrated into regulated workflows safely
- Outputs can be grounded in source documents
- Human review can be incorporated into AI workflows
- Decisions can be fully logged and audited
- AI systems can produce structured, reviewable outputs

---

## Target Users

### Primary User: Compliance Analyst
- Reviews cases and policies
- Uses AI for decision support
- Responsible for final decisions

### Secondary User: Compliance Manager
- Reviews decisions for consistency
- Oversees audit readiness

---

## Core Features

### 1. Document Ingestion

**Description:**
Load and prepare policy documents for retrieval and analysis.

**Capabilities:**
- Load Markdown or text documents
- Split documents into chunks
- Attach metadata (document name, section, chunk ID)
- Store chunks for embedding

**Out of Scope (MVP):**
- PDF parsing
- Large-scale ingestion pipelines
- Automated document updates

---

### 2. Policy Q&A (RAG-Based)

**Description:**
Allow users to ask questions about policies and receive grounded answers.

**Capabilities:**
- Accept natural language questions
- Retrieve relevant document chunks
- Generate answers using retrieved context
- Display citations for all answers

**Success Criteria:**
- Answers reference correct source material
- System avoids hallucinations when context is missing

---

### 3. Case Analysis Workflow

**Description:**
Analyze compliance scenarios using AI-assisted reasoning.

**Capabilities:**
- Accept structured or unstructured case input
- Retrieve relevant policy context
- Generate structured output including:
  - Summary
  - Risk flags
  - Recommended action
  - Supporting sources
  - Confidence level
  - Limitations

**Success Criteria:**
- Output is structured and consistent
- Recommendations are grounded in policy context

---

### 4. Human-in-the-Loop Review

**Description:**
Require human validation before finalizing decisions.

**Capabilities:**
- Display AI-generated recommendations
- Allow user to:
  - Accept
  - Edit
  - Override
- Capture reviewer notes
- Record final decision

**Success Criteria:**
- Every AI output results in a recorded human decision
- Overrides are clearly documented

---

### 5. Audit Logging

**Description:**
Capture a complete record of all interactions and decisions.

**Capabilities:**
- Log:
  - User input
  - Retrieved sources
  - AI output
  - Model used
  - Human decision
  - Reviewer notes
- Store logs in SQLite
- Allow basic retrieval or export of logs

**Success Criteria:**
- Every workflow step is traceable
- Logs can reconstruct the full decision process

---

## MVP User Flows

### Flow 1: Policy Question

1. User submits question
2. System retrieves relevant document chunks
3. AI generates grounded answer
4. System displays answer with citations
5. Interaction is logged

---

### Flow 2: Case Review

1. User submits case scenario
2. System retrieves relevant policy context
3. AI generates structured risk analysis
4. User reviews AI output
5. User accepts, edits, or overrides recommendation
6. Final decision is saved
7. Full interaction is logged

---

## Non-Goals (Out of Scope)

To maintain focus, the following are explicitly out of scope for MVP:

- Custom model training or fine-tuning
- Advanced UI/UX design
- Multi-user authentication or role management
- Real-time collaboration
- Production-grade infrastructure
- Automated decision-making without human review
- Large-scale data ingestion pipelines

---

## Technical Constraints

- Use existing LLM APIs (no model training)
- Use a small set of documents
- Keep infrastructure local or lightweight
- Prioritize clarity over optimization
- Focus on workflow correctness over performance

---

## Risks and Mitigations

### Risk: Hallucinated Responses
**Mitigation:**
- Use retrieval-based grounding (RAG)
- Require citation of sources
- Return “insufficient information” when needed

---

### Risk: Over-reliance on AI Output
**Mitigation:**
- Require human review for all decisions
- Clearly label AI outputs as recommendations

---

### Risk: Lack of Traceability
**Mitigation:**
- Log all inputs, outputs, and decisions
- Store retrieved sources alongside outputs

---

## MVP Success Criteria

The MVP is successful if:

- A user can upload documents and query them
- The system produces grounded, structured AI outputs
- A user can complete a full case review workflow
- All steps are logged and auditable
- The system demonstrates clear AI governance principles

---

## Deliverables

At MVP completion, the project should include:

- Working prototype (CLI or Streamlit)
- Document ingestion and retrieval system
- Case analysis workflow
- Human review interface
- Audit logging system
- Documentation (README, architecture, scope)

---

## Summary

This MVP is designed to demonstrate a realistic, governed AI workflow in a compliance setting.

The focus is not on building a production system, but on proving:

- AI integration into real workflows
- Responsible use of AI in regulated environments
- Clear system design and tradeoff thinking
- End-to-end execution from concept to working prototype
