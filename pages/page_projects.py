"""
page_projects.py — AI Project Recommendation page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import recommend_projects
from core.database import load_latest_skill_gap, log_progress


DIFFICULTY_COLORS = {
    "Beginner": "#34a853",
    "Intermediate": "#fbbc04",
    "Advanced": "#ea4335",
}


def render(session: dict):
    st.header("💡 Project Recommendations")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    career = profile.get("career_goal", "")
    current_skills = profile.get("current_skills", [])

    gap_data = session.get("skill_gap") or load_latest_skill_gap(profile["email"])
    gaps = gap_data.get("gaps", []) if gap_data else []

    st.markdown(
        f"Get portfolio project ideas tailored to **{career}** "
        f"that help you practice both your existing and new skills."
    )
    st.markdown("---")

    if st.button("💡 Get Project Recommendations", type="primary", use_container_width=True):
        with st.spinner("AI is curating project ideas for you... ⏳"):
            projects = recommend_projects(career, current_skills, gaps)
        session["projects"] = projects
        log_progress(profile["email"], "projects_generated", f"For {career}")
        st.success("Project ideas ready!")

    projects = session.get("projects", [])

    if projects:
        st.markdown("---")
        st.markdown(f"## 🚀 Recommended Projects for {career}")

        for i, proj in enumerate(projects, 1):
            difficulty = proj.get("difficulty", "Beginner")
            color = DIFFICULTY_COLORS.get(difficulty, "#1a73e8")

            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #e0e0e0; border-radius:10px; padding:1.2rem;
                            margin-bottom:1rem; border-left:5px solid {color};">
                    <h4 style="margin:0; color:#1a1a1a;">
                        {i}. {proj.get('title', 'Project')}
                        <span style="font-size:0.75rem; background:{color}20; color:{color};
                                     padding:2px 8px; border-radius:12px; margin-left:8px;">
                            {difficulty}
                        </span>
                    </h4>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Description:** {proj.get('description', '—')}")
                    skills_used = proj.get("skills_used", [])
                    if skills_used:
                        st.markdown("**Skills Practiced:** " + "  ".join(f"`{s}`" for s in skills_used))
                with col2:
                    st.metric("⏱️ Time", proj.get("estimated_time", "—"))

                github_idea = proj.get("github_idea", "")
                if github_idea:
                    with st.expander("📁 GitHub Repo Idea"):
                        st.code(github_idea, language=None)

                st.markdown("---")

        # Additional tips
        st.markdown("""
        ### 📌 How to Maximize Your Projects

        1. **Document everything** — Write a clear `README.md` with problem, approach, results
        2. **Deploy it** — Use Streamlit Cloud, Vercel, or Render (all free)
        3. **Add it to LinkedIn** — Link your GitHub repo
        4. **Write about it** — A short blog post on Medium/dev.to gets noticed
        5. **Iterate** — v2 with new features shows growth
        """)
    else:
        st.info("👆 Click the button above to get AI-powered project recommendations.")
        st.markdown("""
        **What you'll get:**
        - 5 personalized project ideas
        - Difficulty level (Beginner / Intermediate / Advanced)
        - Skills each project helps you practice
        - Estimated completion time
        - GitHub repo structure idea
        """)
