"""
page_career.py — Career Analysis page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import analyze_career


def render(session: dict):
    st.header("🎯 Career Analysis")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    st.markdown(f"Analyzing career path for: **{profile.get('career_goal', 'Not set')}**")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Branch:** {profile.get('branch', '—')}")
    with col2:
        st.info(f"**Year:** {profile.get('year', '—')}")
    with col3:
        st.info(f"**Experience:** {profile.get('experience_level', '—')}")

    st.markdown("---")

    # Cache analysis in session to avoid re-calling on every rerun
    cache_key = f"career_analysis_{profile.get('career_goal', '')}_{profile.get('email', '')}"

    if st.button("🔍 Analyze My Career Path", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing your career path... ⏳"):
            result = analyze_career(
                career_goal=profile.get("career_goal", ""),
                branch=profile.get("branch", ""),
                current_skills=profile.get("current_skills", [])
            )
        session[cache_key] = result
        st.success("Analysis complete!")

    if session.get(cache_key):
        st.markdown("### 📊 Career Overview")
        st.markdown(session[cache_key])
    else:
        st.info("👆 Click the button above to generate your personalized career analysis.")
        st.markdown("""
        **What you'll get:**
        - 📌 Role description & responsibilities
        - 📈 Industry demand (India & global)
        - 💰 Salary range (fresher to senior)
        - 🚀 Career progression path
        - 🏢 Key companies hiring
        """)
