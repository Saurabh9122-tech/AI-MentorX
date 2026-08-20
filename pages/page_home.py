"""
page_home.py — Landing / Home page for AI MentorX
"""

import streamlit as st


def render(session: dict):
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem 0;">
        <h1 style="font-size:2.8rem; font-weight:800; color:#1a73e8;">🎓 AI MentorX</h1>
        <p style="font-size:1.2rem; color:#555; max-width:600px; margin:0 auto;">
            Your Personalized AI Career, Skill-Gap & Interview Mentor
        </p>
        <p style="font-size:0.9rem; color:#888; margin-top:0.5rem;">
            AICTE · Edunet Foundation · IBM SkillsBuild Capstone Project
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Feature cards
    cols = st.columns(3)
    features = [
        ("📋", "Smart Profile", "Build your student profile and career goals"),
        ("🔍", "Skill Gap Analysis", "Identify exactly what skills you're missing"),
        ("🗺️", "Personalized Roadmap", "Get a step-by-step learning path"),
        ("🤖", "AI Learning Assistant", "Ask anything about your learning journey"),
        ("📝", "Adaptive Quizzes", "Test your knowledge with AI-generated quizzes"),
        ("🎤", "Mock Interviews", "Practice with realistic AI interview simulations"),
        ("💡", "Project Ideas", "Get portfolio project recommendations"),
        ("📊", "Progress Dashboard", "Track your growth over time"),
        ("🎯", "Career Analysis", "Understand demand, salary, and growth paths"),
    ]

    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#f8f9fa; border-radius:10px; padding:1.2rem;
                        margin-bottom:1rem; border-left:4px solid #1a73e8;">
                <div style="font-size:1.8rem;">{icon}</div>
                <strong>{title}</strong>
                <p style="font-size:0.85rem; color:#666; margin:0.3rem 0 0 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    profile = session.get("profile")
    if profile:
        st.success(f"👋 Welcome back, **{profile['name']}**! "
                   f"Your career goal: **{profile.get('career_goal', 'Not set')}**")
        st.info("➡️ Use the sidebar to navigate to any feature.")
    else:
        st.warning("👆 Start by clicking **Profile** in the sidebar to set up your student profile.")

    # How it works
    with st.expander("📖 How AI MentorX Works", expanded=False):
        st.markdown("""
        **Step-by-step workflow:**

        1. **Profile** — Enter your college details, branch, year, and skills
        2. **Career Analysis** — AI analyzes your target role, demand, and fit
        3. **Skill Gap** — AI identifies which skills you're missing
        4. **Roadmap** — Get a personalized week-by-week learning plan
        5. **AI Assistant** — Chat with your AI mentor anytime
        6. **Quiz** — Test your knowledge on any topic
        7. **Mock Interview** — Practice interview questions with AI feedback
        8. **Projects** — Get portfolio project ideas suited to your level
        9. **Progress** — View your activity, scores, and growth over time

        *All AI features use your profile and career goal to personalize responses.*
        """)

    with st.expander("⚙️ Technical Stack", expanded=False):
        st.markdown("""
        | Component | Technology |
        |---|---|
        | Frontend | Streamlit |
        | AI Backend | Google Gemini 1.5 Flash (free tier) |
        | Database | SQLite (local) |
        | Language | Python 3.10+ |
        | Deployment | Streamlit Community Cloud |
        | Source Control | GitHub |
        """)
