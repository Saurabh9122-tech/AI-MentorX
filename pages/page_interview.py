"""
page_interview.py — AI Mock Interview page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import get_interview_question, evaluate_interview_answer
from core.database import save_interview_log, load_interview_history


ROUND_TYPES = [
    "Technical – Core Concepts",
    "Technical – Problem Solving / DSA",
    "Behavioral / HR",
    "System Design",
    "Project Discussion",
]


def render(session: dict):
    st.header("🎤 AI Mock Interview")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    career = profile.get("career_goal", "")

    st.markdown(
        f"Practice realistic interview questions for **{career}** "
        f"and get instant AI feedback on your answers."
    )
    st.markdown("---")

    # Session state for interview
    if "interview_questions_asked" not in session:
        session["interview_questions_asked"] = []
    if "interview_current_q" not in session:
        session["interview_current_q"] = None
    if "interview_evaluation" not in session:
        session["interview_evaluation"] = None

    # Settings
    col1, col2 = st.columns(2)
    with col1:
        round_type = st.selectbox("Interview Round Type", ROUND_TYPES)
    with col2:
        st.markdown("")
        st.markdown("")
        questions_asked = len(session["interview_questions_asked"])
        st.info(f"Questions asked this session: **{questions_asked}**")

    # Get next question
    if st.button("❓ Get Next Question", type="primary", use_container_width=True):
        with st.spinner("Generating interview question..."):
            q = get_interview_question(
                career_goal=career,
                round_type=round_type,
                previous_questions=session["interview_questions_asked"]
            )
        session["interview_current_q"] = q
        session["interview_evaluation"] = None
        st.rerun()

    # Display current question and answer form
    current_q = session.get("interview_current_q")
    if current_q:
        st.markdown("---")
        st.markdown("### 💬 Interview Question")
        st.info(f"**{current_q}**")

        with st.form("interview_form"):
            answer = st.text_area(
                "Your Answer",
                placeholder="Type your answer here... (aim for 3-5 sentences with specific examples)",
                height=150
            )
            col1, col2 = st.columns(2)
            with col1:
                eval_btn = st.form_submit_button("📊 Submit & Get Feedback", type="primary",
                                                  use_container_width=True)
            with col2:
                skip_btn = st.form_submit_button("⏭️ Skip This Question",
                                                  use_container_width=True)

        if eval_btn and answer.strip():
            with st.spinner("AI is evaluating your answer..."):
                evaluation = evaluate_interview_answer(current_q, answer, career)
            session["interview_evaluation"] = evaluation

            # Save to DB
            score = evaluation.get("score", 0)
            if not isinstance(score, int):
                try:
                    score = int(score)
                except (ValueError, TypeError):
                    score = 0
            save_interview_log(
                email=profile["email"],
                career_goal=career,
                question=current_q,
                answer=answer,
                feedback=evaluation.get("feedback", ""),
                score=score
            )
            session["interview_questions_asked"].append(current_q)
            st.rerun()

        elif eval_btn and not answer.strip():
            st.warning("Please type an answer before submitting.")

        if skip_btn:
            session["interview_questions_asked"].append(current_q + " [SKIPPED]")
            session["interview_current_q"] = None
            session["interview_evaluation"] = None
            st.rerun()

    # Show evaluation
    evaluation = session.get("interview_evaluation")
    if evaluation:
        st.markdown("---")
        st.markdown("### 📊 AI Feedback")

        score = evaluation.get("score", 0)
        if not isinstance(score, int):
            try:
                score = int(score)
            except (ValueError, TypeError):
                score = 0

        # Score bar
        score_pct = score / 10
        col1, col2 = st.columns([1, 3])
        with col1:
            color = "#34a853" if score >= 7 else "#fbbc04" if score >= 5 else "#ea4335"
            st.markdown(f"""
            <div style="text-align:center; padding:1rem; background:{color}20;
                        border-radius:8px; border:2px solid {color};">
                <div style="font-size:2rem; font-weight:800; color:{color};">{score}/10</div>
                <div style="font-size:0.8rem; color:#555;">Score</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.progress(score_pct, text=f"Performance: {score}/10")
            feedback = evaluation.get("feedback", "No feedback available.")
            st.markdown(f"**📝 Feedback:** {feedback}")

        improved = evaluation.get("improved_answer", "")
        if improved:
            with st.expander("💡 See a stronger example answer"):
                st.markdown(improved)

        st.markdown("---")
        if st.button("➡️ Next Question", type="primary"):
            session["interview_current_q"] = None
            session["interview_evaluation"] = None
            st.rerun()

    # Interview tips
    if not current_q and not evaluation:
        with st.expander("💡 Interview Tips", expanded=True):
            st.markdown("""
            **STAR Method for Behavioral Questions:**
            - **S**ituation — Describe the context
            - **T**ask — What was your responsibility
            - **A**ction — What did you do specifically
            - **R**esult — What was the outcome

            **Technical Questions:**
            - Think aloud — interviewers want to hear your reasoning
            - Start with brute force, then optimize
            - Ask clarifying questions before diving in

            **General Tips:**
            - Be specific — avoid vague answers
            - Use examples from projects/coursework
            - Keep answers focused (2-3 minutes max)
            """)

    # History
    st.markdown("---")
    st.markdown("#### 📜 Recent Interview Sessions")
    history = load_interview_history(profile["email"])
    if history:
        for h in history[:5]:
            score_val = h.get("score", 0)
            color = "🟢" if score_val >= 7 else "🟡" if score_val >= 5 else "🔴"
            st.markdown(
                f"{color} **Q:** {h['question'][:70]}…  "
                f"| Score: **{score_val}/10** | *{h['logged_at'][:10]}*"
            )
    else:
        st.info("No interview history yet. Click 'Get Next Question' to start!")
