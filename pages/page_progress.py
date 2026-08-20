"""
page_progress.py — Student Progress Dashboard
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import generate_overall_feedback
from core.database import load_progress, load_quiz_history, load_interview_history


ACTION_ICONS = {
    "profile_updated": "👤",
    "skill_gap_analyzed": "🔍",
    "quiz_completed": "📝",
    "interview_question": "🎤",
    "assistant_chat": "🤖",
    "projects_generated": "💡",
    "roadmap_generated": "🗺️",
}


def render(session: dict):
    st.header("📊 Progress Dashboard")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    email = profile["email"]
    quiz_history = load_quiz_history(email)
    interview_history = load_interview_history(email)
    activity_log = load_progress(email)

    # ── Top Metrics ───────────────────────────────────────────────────────────
    st.markdown("### 📈 Overview")
    m1, m2, m3, m4 = st.columns(4)

    quizzes_taken = len(quiz_history)
    avg_quiz_score = (
        sum(r["score"] / max(r["total"], 1) * 100 for r in quiz_history) / quizzes_taken
        if quizzes_taken else 0
    )
    interviews_done = len(interview_history)
    interview_scores = [r.get("score", 0) for r in interview_history if r.get("score")]
    avg_interview = sum(interview_scores) / len(interview_scores) if interview_scores else 0

    m1.metric("📝 Quizzes Taken", quizzes_taken)
    m2.metric("📊 Avg Quiz Score", f"{avg_quiz_score:.0f}%")
    m3.metric("🎤 Interview Rounds", interviews_done)
    m4.metric("⭐ Avg Interview Score", f"{avg_interview:.1f}/10")

    st.markdown("---")

    # ── Profile completeness ──────────────────────────────────────────────────
    st.markdown("### ✅ Profile Completeness")
    p = profile
    checks = {
        "Name & Email": bool(p.get("name") and p.get("email")),
        "College & Branch": bool(p.get("college") and p.get("branch")),
        "Career Goal Set": bool(p.get("career_goal")),
        "Skills Entered": len(p.get("current_skills", [])) > 0,
        "Skill Gap Analyzed": bool(session.get("skill_gap") or load_quiz_history(email)),
        "At Least 1 Quiz": quizzes_taken > 0,
        "At Least 1 Interview": interviews_done > 0,
    }
    completed = sum(1 for v in checks.values() if v)
    total_checks = len(checks)
    st.progress(completed / total_checks, text=f"{completed}/{total_checks} milestones completed")

    cols = st.columns(4)
    for i, (label, done) in enumerate(checks.items()):
        with cols[i % 4]:
            icon = "✅" if done else "⬜"
            st.markdown(f"{icon} {label}")

    st.markdown("---")

    # ── Quiz Performance ──────────────────────────────────────────────────────
    if quiz_history:
        st.markdown("### 📝 Quiz Performance")
        rows = []
        for h in quiz_history[:10]:
            rows.append({
                "Topic": h["topic"],
                "Score": f"{h['score']}/{h['total']}",
                "Percentage": f"{h['score']/max(h['total'],1)*100:.0f}%",
                "Date": h["taken_at"][:10],
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Interview Performance ─────────────────────────────────────────────────
    if interview_history:
        st.markdown("### 🎤 Interview Performance")
        irows = []
        for h in interview_history[:10]:
            irows.append({
                "Question": h["question"][:60] + "…" if len(h["question"]) > 60 else h["question"],
                "Score": f"{h.get('score', 0)}/10",
                "Date": h["logged_at"][:10],
            })
        df2 = pd.DataFrame(irows)
        st.dataframe(df2, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Activity Log ──────────────────────────────────────────────────────────
    st.markdown("### 🕐 Recent Activity")
    if activity_log:
        for entry in activity_log[:15]:
            icon = ACTION_ICONS.get(entry["action"], "•")
            dt = entry["logged_at"][:16].replace("T", " ")
            st.markdown(f"{icon} **{entry['detail']}** — *{dt}*")
    else:
        st.info("Your activity will appear here as you use AI MentorX.")

    st.markdown("---")

    # ── AI Feedback Report ────────────────────────────────────────────────────
    st.markdown("### 🎯 AI Progress Report")
    if st.button("📋 Generate AI Feedback Report", type="primary", use_container_width=True):
        with st.spinner("AI is preparing your personalized progress report... ⏳"):
            report = generate_overall_feedback(profile, quiz_history, interview_history)
        session["progress_report"] = report
        st.rerun()

    if session.get("progress_report"):
        st.markdown(session["progress_report"])
    else:
        st.info("Click the button above to get a personalized AI analysis of your progress.")
