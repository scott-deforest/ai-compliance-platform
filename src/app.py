import streamlit as st

from qa import answer_policy_question_with_sources
from case_analysis import analyze_case_with_sources
from audit import initialize_database, log_interaction, get_audit_log


st.set_page_config(
    page_title="AI Compliance & Risk Intelligence Platform",
    page_icon="⚖️",
    layout="wide",
)

initialize_database()

st.title("AI Compliance & Risk Intelligence Platform")
st.caption(
    "A governed AI workflow prototype for compliance decision support, "
    "with grounded retrieval, human review, and audit logging."
)

tab_qa, tab_case, tab_audit = st.tabs(["Policy Q&A", "Case Analysis", "Audit Log"])

with tab_qa:
    st.header("Policy Q&A")
    st.write("Ask a question about the loaded policy documents.")

    question = st.text_area(
        "Policy Question",
        placeholder="Example: When should a case be escalated?",
        height=100,
    )

    if st.button("Ask Policy Question"):
        if not question.strip():
            st.warning("Please enter a policy question.")
        else:
            with st.spinner("Retrieving policy context and generating answer..."):
                result = answer_policy_question_with_sources(question)

            st.subheader("AI Answer")
            st.write(result["answer"])

            st.subheader("Retrieved Sources")

            for index, source in enumerate(result["sources"], start=1):
                metadata = source["metadata"]

                document_name = metadata.get(
                    "document_name",
                    "Unknown document"
                )

                section = metadata.get(
                    "section",
                    "Unknown section"
                )

                relative_path = metadata.get(
                    "relative_path",
                    ""
                )

                with st.expander(f"Source {index}: {document_name}"):

                    st.write(f"**Document:** {document_name}")
                    st.write(f"**Section:** {section}")

                    if relative_path:
                        st.write(f"**Path:** {relative_path}")

                    st.write(f"**Chunk ID:** {source['id']}")

                    st.text(source["document"][:1500])

with tab_case:
    st.header("Compliance Case Analysis")
    st.write("Submit a case scenario for AI-assisted review.")

    case_text = st.text_area(
        "Case Scenario",
        placeholder=(
            "Example: Customer initiated multiple high-value wire transfers "
            "from newly linked external accounts over a 48-hour period..."
        ),
        height=150,
    )

    if st.button("Analyze Case"):
        if not case_text.strip():
            st.warning("Please enter a case scenario.")
        else:
            with st.spinner("Analyzing case against policy context..."):
                st.session_state["case_text"] = case_text
                case_result = analyze_case_with_sources(case_text)
                st.session_state["ai_output"] = case_result["analysis"]
                st.session_state["case_sources"] = case_result["sources"]

    if "ai_output" in st.session_state:
        st.subheader("AI Case Analysis")
        st.write(st.session_state["ai_output"])

        if "case_sources" in st.session_state:
            st.subheader("Retrieved Sources")

            for index, source in enumerate(st.session_state["case_sources"], start=1):
                metadata = source["metadata"]

                document_name = metadata.get(
                    "document_name",
                    "Unknown document"
                )

                section = metadata.get(
                    "section",
                    "Unknown section"
                )

                relative_path = metadata.get(
                    "relative_path",
                    ""
                )

                with st.expander(f"Source {index}: {document_name}"):

                    st.write(f"**Document:** {document_name}")
                    st.write(f"**Section:** {section}")

                    if relative_path:
                        st.write(f"**Path:** {relative_path}")

                    st.write(f"**Chunk ID:** {source['id']}")

                    st.text(source["document"][:1500])

            st.subheader("Human Review")

            human_decision = st.selectbox(
                "Final Decision",
                ["Accept", "Escalate", "Reject", "Needs More Review"],
            )

            reviewer_notes = st.text_area(
                "Reviewer Notes",
                placeholder="Document rationale for the final decision...",
                height=100,
            )

            if st.button("Save Review to Audit Log"):
                log_interaction(
                    workflow_type="case_analysis",
                    user_input=st.session_state["case_text"],
                    ai_output=st.session_state["ai_output"],
                    human_decision=human_decision,
                    reviewer_notes=reviewer_notes,
                )

                st.success("Review saved to audit log.")

with tab_audit:
    st.header("Audit Log")
    st.write("All logged interactions — policy Q&A and case analysis decisions.")

    if st.button("Refresh"):
        st.rerun()

    rows = get_audit_log()

    if not rows:
        st.info("No interactions logged yet.")
    else:
        for row in rows:
            id_, timestamp, workflow_type, user_input, ai_output, human_decision, reviewer_notes = row
            label = f"#{id_} | {timestamp[:19]} | {workflow_type} | Decision: {human_decision}"
            with st.expander(label):
                st.markdown("**User Input**")
                st.write(user_input)
                st.markdown("**AI Output**")
                st.write(ai_output)
                if reviewer_notes:
                    st.markdown("**Reviewer Notes**")
                    st.write(reviewer_notes)