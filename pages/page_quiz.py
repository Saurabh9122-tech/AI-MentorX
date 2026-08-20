"""
page_quiz.py — AI-generated adaptive quiz page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import generate_quiz
from core.database import save_quiz_result, load_quiz_history


DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]


def render(session: dict):
    st.header("📝 Adaptive Quiz")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    career = profile.get("career_goal", "")

    st.markdown("Test your knowledge with AI-generated questions tailored to your career goal.")
    st.markdown("---")

    # Quiz configuration
    col1, col2, col3 = st.columns(3)
    with col1:
        # Suggest topics from career goal and skill gaps
        gap_data = session.get("skill_gap")
        suggestions = []
        if gap_data:
            suggestions = gap_data.get("priority_order", [])[:5]
        if not suggestions:
            suggestions = [career, "Python", "Data Structures", "SQL", "System Design"]
        topic = st.selectbox("Topic", suggestions + ["Custom topic below"])
        custom_topic = st.text_input("Or enter a custom topic", placeholder="e.g. Neural Networks")
        final_topic = custom_topic.strip() if custom_topic.strip() else topic

    with col2:
        difficulty = st.selectbox("Difficulty", DIFFICULTIES)

    with col3:
        num_q = st.selectbox("Number of Questions", [3, 5, 10], index=1)

    if st.button("🚀 Generate Quiz", type="primary", use_container_width=True):
        with st.spinner(f"Generating {num_q} {difficulty} questions on '{final_topic}'... ⏳"):
            questions = generate_quiz(final_topic, difficulty, num_q)
        session["quiz_questions"] = questions
        session["quiz_topic"] = final_topic
        session["quiz_answers"] = {}
        session["quiz_submitted"] = False
        st.success(f"Quiz ready! {len(questions)} questions on **{final_topic}**")
        st.rerun()

    # Active quiz
    questions = session.get("quiz_questions", [])
    if questions and not session.get("quiz_submitted", False):
        st.markdown("---")
        st.markdown(f"### 📋 Quiz: {session.get('quiz_topic', '')} ({difficulty})")

        with st.form("quiz_form"):
            answers = {}
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}. {q.get('question', '')}**")
                options = q.get("options", [])
                if options:
                    ans = st.radio(
                        f"Select your answer for Q{i+1}",
                        options,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    answers[i] = ans
                st.markdown("")

            submitted = st.form_submit_button("✅ Submit Quiz", type="primary", use_container_width=True)

        if submitted:
            session["quiz_answers"] = answers
            session["quiz_submitted"] = True
            st.rerun()

    # Results
    if session.get("quiz_submitted") and questions:
        st.markdown("---")
        st.markdown("### 🏆 Quiz Results")
        answers = session.get("quiz_answers", {})
        score = 0
        details = []

        for i, q in enumerate(questions):
            correct = q.get("answer", "")
            user_ans = answers.get(i, "")
            is_correct = user_ans.strip() == correct.strip()
            if is_correct:
                score += 1
            details.append({
                "question": q.get("question", ""),
                "user_answer": user_ans,
                "correct_answer": correct,
                "correct": is_correct,
                "explanation": q.get("explanation", "")
            })

        total = len(questions)
        pct = score / total * 100

        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{score}/{total}")
        c2.metric("Percentage", f"{pct:.0f}%")
        grade = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "D"
        c3.metric("Grade", grade)

        st.progress(pct / 100, text=f"{pct:.0f}% correct")

        # Save to DB
        topic_name = session.get("quiz_topic", "Unknown")
        save_quiz_result(profile["email"], topic_name, score, total, details)

        # Detailed review
        st.markdown("#### 📖 Answer Review")
        for i, d in enumerate(details):
            if d["correct"]:
                st.success(f"✅ **Q{i+1}:** {d['question']}\n\n"
                           f"Your answer: **{d['user_answer']}** ✓")
            else:
                st.error(f"❌ **Q{i+1}:** {d['question']}\n\n"
                         f"Your answer: {d['user_answer']}  |  "
                         f"Correct: **{d['correct_answer']}**")
            if d.get("explanation"):
                st.caption(f"💡 {d['explanation']}")

        if st.button("🔄 Take Another Quiz", use_container_width=True):
            for key in ["quiz_questions", "quiz_answers", "quiz_submitted", "quiz_topic"]:
                session.pop(key, None)
            st.rerun()

    # Quiz history
    st.markdown("---")
    st.markdown("#### 📜 Quiz History")
    history = load_quiz_history(profile["email"])
    if history:
        for h in history[:5]:
            pct = h["score"] / max(h["total"], 1) * 100
            st.markdown(
                f"• **{h['topic']}** — {h['score']}/{h['total']} ({pct:.0f}%) "
                f"— *{h['taken_at'][:10]}*"
            )
    else:
        st.info("No quiz history yet. Take your first quiz above!")
