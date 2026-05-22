import streamlit as st

from qa import answer_policy_question
from case_analysis import analyze_case
from audit import initialize_database, log_interaction


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

tab_qa, tab_case = st.tabs(["Policy Q&A", "Case Analysis"])

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
                answer = answer_policy_question(question)

            st.subheader("AI Answer")
            st.write(answer)

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
                st.session_state["ai_output"] = analyze_case(case_text)

    if "ai_output" in st.session_state:
        st.subheader("AI Case Analysis")
        st.write(st.session_state["ai_output"])

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