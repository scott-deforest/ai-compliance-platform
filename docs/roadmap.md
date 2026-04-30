# Roadmap

## Overview

This roadmap outlines the development plan for the AI Compliance & Risk Intelligence Platform MVP.

The goal is to move from concept → working prototype in a structured, iterative way, focusing on:

- Real functionality over polish
- Incremental delivery
- Demonstrable outcomes at each stage

The roadmap is organized into **focused sprints**, each delivering a tangible, testable capability.

---

## Development Approach

- Time commitment: ~45–60 minutes per day
- Build in small, testable increments
- Prioritize working functionality over perfection
- Commit progress frequently
- Document decisions as you go

---

## Sprint 1 — Document Ingestion & Policy Q&A (RAG Foundation)

### Goal

Enable users to load documents and ask questions with grounded, citation-based answers.

This is the foundation of the entire system.

---

### Key Deliverables

- Load policy documents (Markdown / TXT)
- Split documents into chunks
- Generate embeddings for each chunk
- Store embeddings in vector store
- Accept user questions
- Retrieve relevant chunks
- Generate answers using retrieved context
- Display answers with source references

---

### Tasks

- [ ] Set up project structure in `src/`
- [ ] Load and read document files
- [ ] Implement document chunking logic
- [ ] Integrate embedding generation (LLM API)
- [ ] Store embeddings in vector database (ChromaDB)
- [ ] Build retrieval function (top-k matching chunks)
- [ ] Create prompt template for grounded Q&A
- [ ] Call LLM API for answer generation
- [ ] Return answer with referenced sources

---

### Success Criteria

- User can ask a question and receive an answer
- Answer is based on retrieved document content
- Sources are clearly referenced
- System avoids hallucination when context is missing

---

### Output

- Working CLI or simple interface
- Demonstration of grounded policy Q&A

---

## Sprint 2 — Case Analysis Workflow

### Goal

Enable AI-assisted analysis of compliance scenarios.

---

### Key Deliverables

- Accept case/scenario input
- Retrieve relevant policy context
- Generate structured risk analysis output

---

### Tasks

- [ ] Define structured output schema
- [ ] Build case input handler
- [ ] Reuse retrieval layer from Sprint 1
- [ ] Create prompt template for risk analysis
- [ ] Generate structured AI response
- [ ] Display structured output clearly

---

### Success Criteria

- AI produces consistent, structured outputs
- Outputs include:
  - Summary
  - Risk flags
  - Recommended action
  - Supporting sources
  - Confidence / limitations
- Output is grounded in policy context

---

### Output

- End-to-end case analysis prototype

---

## Sprint 3 — Human-in-the-Loop Review

### Goal

Introduce controlled decision-making with human oversight.

---

### Key Deliverables

- Allow users to review AI output
- Capture final decision (accept/edit/override)
- Record reviewer notes

---

### Tasks

- [ ] Build review interface (CLI or Streamlit)
- [ ] Implement decision options:
  - Accept
  - Edit
  - Override
- [ ] Capture reviewer notes
- [ ] Store final decision data

---

### Success Criteria

- Every AI output requires human decision
- Overrides are clearly captured
- Final decisions are stored consistently

---

### Output

- Governed AI workflow with human validation

---

## Sprint 4 — Audit Logging System

### Goal

Create full traceability of all system interactions.

---

### Key Deliverables

- Log all workflows and decisions
- Store logs in structured format (SQLite)

---

### Tasks

- [ ] Define audit log schema
- [ ] Set up SQLite database
- [ ] Log:
  - User input
  - Retrieved sources
  - AI output
  - Model used
  - Human decision
  - Reviewer notes
- [ ] Implement log retrieval or export

---

### Success Criteria

- Every interaction is recorded
- Logs can reconstruct full decision flow
- System demonstrates auditability

---

### Output

- Queryable audit log system

---

## Sprint 5 — UI & Workflow Refinement (Optional but High Value)

### Goal

Improve usability and demo-ability of the system.

---

### Key Deliverables

- Streamlit UI for:
  - Document upload
  - Q&A interface
  - Case submission
  - Review workflow
  - Audit viewing

---

### Tasks

- [ ] Build Streamlit interface
- [ ] Connect backend workflows
- [ ] Improve display of outputs
- [ ] Add basic navigation between workflows

---

### Success Criteria

- End-to-end demo can be run visually
- System is easy to explain in interviews

---

### Output

- Demo-ready application

---

## Suggested Timeline

| Sprint | Focus | Duration |
|-------|------|----------|
| Sprint 1 | RAG Foundation | 1–2 weeks |
| Sprint 2 | Case Analysis | 1–2 weeks |
| Sprint 3 | Human Review | 1 week |
| Sprint 4 | Audit Logging | 1 week |
| Sprint 5 | UI Refinement | 1 week |

Total: ~6–8 weeks (at part-time pace)

---

## Definition of Done (MVP)

The MVP is complete when:

- Documents can be loaded and queried
- AI outputs are grounded and structured
- Users can complete a full case workflow
- Human decisions are captured
- All interactions are logged
- System can be demonstrated end-to-end

---

## Execution Principles

- Build → Test → Iterate
- Don’t over-engineer early
- Focus on working systems
- Prioritize clarity over complexity
- Treat this like a real product, not a tutorial

---

## Summary

This roadmap transforms the project from concept into a working AI-powered system.

Each sprint delivers a meaningful capability and builds toward a complete, demonstrable product that showcases:

- AI system design
- Product thinking
- Governance and risk awareness
- Practical execution
