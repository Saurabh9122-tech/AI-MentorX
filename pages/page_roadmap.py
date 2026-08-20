"""
page_roadmap.py — Personalized Learning Roadmap page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.ai_engine import generate_roadmap
from core.database import load_latest_skill_gap, save_skill_gap


PHASE_COLORS = ["#1a73e8", "#34a853", "#fbbc04", "#ea4335", "#9334e6", "#00acc1", "#e67e22"]


def render(session: dict):
    st.header("🗺️ Personalized Learning Roadmap")

    profile = session.get("profile")
    if not profile:
        st.warning("⚠️ Please complete your **Profile** first.")
        return

    career = profile.get("career_goal", "")
    year = profile.get("year", 1)

    # Get gaps
    gap_data = session.get("skill_gap") or load_latest_skill_gap(profile["email"])
    gaps = gap_data.get("gaps", []) if gap_data else []

    if not gaps:
        st.info("ℹ️ Run the **Skill Gap Analysis** first to get a tailored roadmap. "
                "Or click below to generate a general roadmap.")

    st.markdown(f"**Career Goal:** {career} &nbsp;|&nbsp; **Year:** {year} &nbsp;|&nbsp; "
                f"**Gaps to address:** {len(gaps)}")
    st.markdown("---")

    if st.button("🗺️ Generate My Learning Roadmap", type="primary", use_container_width=True):
        with st.spinner("AI is building your personalized roadmap... ⏳"):
            roadmap = generate_roadmap(
                career_goal=career,
                gaps=gaps if gaps else [career + " fundamentals"],
                year=year
            )
        session["roadmap"] = roadmap

        # Persist to DB (update latest skill gap entry's roadmap)
        sg = load_latest_skill_gap(profile["email"])
        if sg:
            save_skill_gap(profile["email"], career, sg.get("gaps", []), roadmap)
        else:
            save_skill_gap(profile["email"], career, [], roadmap)

        st.success("Roadmap generated!")

    roadmap = session.get("roadmap")
    if not roadmap and gap_data:
        roadmap = gap_data.get("roadmap", [])

    if roadmap:
        st.markdown("---")
        st.markdown("## 🚀 Your Learning Roadmap")

        for i, phase in enumerate(roadmap):
            color = PHASE_COLORS[i % len(PHASE_COLORS)]
            with st.expander(
                f"{''.join(['■']*1)} **{phase.get('phase', f'Phase {i+1}')}** "
                f"— {phase.get('duration', '')}",
                expanded=(i == 0)
            ):
                st.markdown(f"**Topic:** {phase.get('topic', '—')}")
                st.markdown(f"**What to learn:** {phase.get('description', '—')}")

                resources = phase.get("resources", [])
                if resources:
                    st.markdown("**📚 Free Resources:**")
                    for r in resources:
                        st.markdown(f"  - {r}")

                milestone = phase.get("milestone", "")
                if milestone:
                    st.success(f"🏁 **Milestone:** {milestone}")

        st.markdown("---")
        st.markdown("""
        > 💡 **Tip:** Bookmark this roadmap. Use the **AI Assistant** tab to ask questions
        > about any topic in your roadmap. Use the **Quiz** tab to test yourself on completed phases.
        """)
    else:
        st.info("👆 Click the button above to generate your roadmap.")
        st.markdown("""
        **Your roadmap will include:**
        - Week-by-week phases
        - Topic descriptions
        - Free learning resources (YouTube, Coursera, Kaggle, freeCodeCamp)
        - Milestone checkpoints
        """)
