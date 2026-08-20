"""
page_assistant.py — AI Learning Assistant (chat interface)
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import ask_learning_assistant
from core.database import log_progress


def render(session: dict):
    st.header("🤖 AI Learning Assistant")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    career = profile.get("career_goal", "your career goal")
    skills = profile.get("current_skills", [])

    st.markdown(
        f"Ask me anything about **{career}**, learning resources, concepts, or career advice. "
        f"I'll personalize my answers based on your profile."
    )
    st.markdown("---")

    # Initialize chat history in session
    if "chat_history" not in session:
        session["chat_history"] = []

    # Suggested prompts
    st.markdown("**💡 Quick Questions:**")
    suggestions = [
        f"What are the most important topics to learn for {career}?",
        f"Explain the difference between supervised and unsupervised learning simply.",
        f"How do I build a strong portfolio for {career}?",
        f"What Python libraries should I master for {career}?",
        f"How do I prepare for technical interviews at top companies?",
    ]
    cols = st.columns(len(suggestions[:3]))
    for i, sug in enumerate(suggestions[:3]):
        with cols[i]:
            if st.button(sug[:55] + "…" if len(sug) > 55 else sug,
                         key=f"sug_{i}", use_container_width=True):
                session["pending_question"] = sug

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in session["chat_history"]:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["text"])
            else:
                with st.chat_message("assistant", avatar="🎓"):
                    st.markdown(msg["text"])

    # Handle pending question from quick-select buttons
    pending = session.pop("pending_question", None)

    # Chat input
    user_input = st.chat_input("Ask your AI mentor a question…")

    question = user_input or pending
    if question:
        # Add user message
        session["chat_history"].append({"role": "user", "text": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("Thinking…"):
                response = ask_learning_assistant(
                    question=question,
                    career_goal=career,
                    current_skills=skills,
                    chat_history=session["chat_history"][:-1]  # exclude the current question
                )
            st.markdown(response)

        session["chat_history"].append({"role": "ai", "text": response})
        log_progress(profile["email"], "assistant_chat", f"Q: {question[:80]}")
        st.rerun()

    if session["chat_history"]:
        if st.button("🗑️ Clear Chat History", use_container_width=False):
            session["chat_history"] = []
            st.rerun()
