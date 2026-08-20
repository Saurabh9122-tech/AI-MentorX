"""
page_skillgap.py — Skill Gap Analysis page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import analyze_skill_gap
from core.database import save_skill_gap, load_latest_skill_gap


def render(session: dict):
    st.header("🔍 Skill Gap Analysis")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    career = profile.get("career_goal", "")
    current_skills = profile.get("current_skills", [])

    st.markdown(f"Comparing your skills against requirements for **{career}**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Your Current Skills:**")
        if current_skills:
            for s in current_skills:
                st.markdown(f"✅ {s}")
        else:
            st.markdown("*No skills listed yet — update your profile.*")

    with col2:
        st.markdown("**What We'll Analyze:**")
        st.markdown(f"""
        - Required skills for **{career}**
        - Skills you already have ✅
        - Skills you're missing ❌
        - Priority learning order 📋
        """)

    st.markdown("---")

    if st.button("🧠 Run Skill Gap Analysis", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing your skill gaps... ⏳"):
            result = analyze_skill_gap(
                career_goal=career,
                current_skills=current_skills,
                branch=profile.get("branch", ""),
                year=profile.get("year", 1)
            )
        # Save to DB and session
        save_skill_gap(
            email=profile["email"],
            career_goal=career,
            gaps=result.get("gaps", []),
            roadmap=[]  # roadmap generated separately
        )
        session["skill_gap"] = result
        st.success("Skill gap analysis complete!")

    # Load from session or DB
    gap_data = session.get("skill_gap") or load_latest_skill_gap(profile["email"])

    if gap_data:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        required = gap_data.get("required_skills", [])
        gaps = gap_data.get("gaps", [])
        strengths = gap_data.get("strengths", [])
        priorities = gap_data.get("priority_order", gaps)

        # Metrics row
        m1, m2, m3 = st.columns(3)
        m1.metric("✅ Skills You Have", len(strengths))
        m2.metric("❌ Skills to Learn", len(gaps))
        m3.metric("📋 Total Required", len(required))

        # Progress bar
        if required:
            progress = len(strengths) / len(required)
            st.progress(progress, text=f"Skill completion: {progress*100:.0f}%")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ✅ Your Strengths")
            if strengths:
                for s in strengths:
                    st.success(f"✅ {s}")
            else:
                st.info("Keep learning — every expert was once a beginner!")

        with col2:
            st.markdown("#### ❌ Skill Gaps")
            if gaps:
                for g in gaps:
                    st.error(f"❌ {g}")
            else:
                st.success("🎉 You have all required skills!")

        if priorities:
            st.markdown("#### 📋 Recommended Learning Order")
            for i, skill in enumerate(priorities, 1):
                st.markdown(f"**{i}.** {skill}")

        st.info("👉 Go to the **Roadmap** tab to get a week-by-week learning plan for these gaps.")
    else:
        st.info("👆 Click the button above to analyze your skill gaps.")
