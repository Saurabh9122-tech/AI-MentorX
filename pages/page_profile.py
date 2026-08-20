"""
page_profile.py — Student profile creation and editing
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.database import save_profile, load_profile

BRANCHES = [
    "Computer Science & Engineering",
    "Information Technology",
    "Electronics & Communication Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Biotechnology",
    "Data Science",
    "Artificial Intelligence & ML",
    "Other",
]

CAREER_GOALS = [
    "Data Scientist",
    "Machine Learning Engineer",
    "Software Developer (Full Stack)",
    "Frontend Developer",
    "Backend Developer",
    "DevOps / Cloud Engineer",
    "Cybersecurity Analyst",
    "Data Analyst",
    "AI/NLP Engineer",
    "Mobile App Developer (Android/iOS)",
    "Embedded Systems Engineer",
    "Product Manager",
    "UI/UX Designer",
    "Blockchain Developer",
    "Other (specify below)",
]

EXPERIENCE_LEVELS = ["Beginner (0–6 months)", "Intermediate (6 months–2 years)", "Advanced (2+ years)"]

COMMON_SKILLS = [
    "Python", "Java", "C++", "C", "JavaScript", "TypeScript", "HTML/CSS",
    "SQL", "MongoDB", "React", "Node.js", "Django", "Flask", "FastAPI",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
    "Data Analysis", "Pandas", "NumPy", "Matplotlib", "Power BI", "Tableau",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Linux",
    "Statistics", "Probability", "Computer Networks", "Operating Systems",
    "Data Structures & Algorithms", "System Design", "REST APIs", "GraphQL",
    "Android (Kotlin/Java)", "iOS (Swift)", "Flutter", "React Native",
]


def render(session: dict):
    st.header("📋 Student Profile")
    st.markdown("Fill in your details so AI MentorX can personalize everything for you.")

    # Pre-fill if profile exists
    existing = session.get("profile") or {}

    with st.form("profile_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *", value=existing.get("name", ""),
                                  placeholder="e.g. Priya Sharma")
            email = st.text_input("Email Address *", value=existing.get("email", ""),
                                   placeholder="e.g. priya@college.edu")
            college = st.text_input("College / University", value=existing.get("college", ""),
                                     placeholder="e.g. IIT Delhi")

        with col2:
            branch = st.selectbox("Branch / Stream", BRANCHES,
                                   index=BRANCHES.index(existing.get("branch", BRANCHES[0]))
                                   if existing.get("branch") in BRANCHES else 0)
            year = st.selectbox("Current Year of Study", [1, 2, 3, 4],
                                 index=(existing.get("year", 1) - 1))
            exp_level = st.selectbox("Experience Level", EXPERIENCE_LEVELS,
                                      index=next(
                                          (i for i, e in enumerate(EXPERIENCE_LEVELS)
                                           if e == existing.get("experience_level")), 0
                                      ))

        st.markdown("#### 🎯 Career Goal")
        career_goal_choice = st.selectbox(
            "Target Career Role *", CAREER_GOALS,
            index=CAREER_GOALS.index(existing.get("career_goal", CAREER_GOALS[0]))
            if existing.get("career_goal") in CAREER_GOALS else 0
        )
        custom_career = ""
        if career_goal_choice == "Other (specify below)":
            custom_career = st.text_input("Specify your career goal",
                                           value=existing.get("career_goal", "")
                                           if existing.get("career_goal") not in CAREER_GOALS else "")

        st.markdown("#### 🛠️ Current Skills")
        st.caption("Select all skills you already know (at least basic level).")

        existing_skills = existing.get("current_skills", [])
        selected_skills = st.multiselect(
            "Select from common skills",
            COMMON_SKILLS,
            default=[s for s in existing_skills if s in COMMON_SKILLS]
        )
        custom_skills_raw = st.text_input(
            "Add other skills (comma-separated)",
            value=", ".join(s for s in existing_skills if s not in COMMON_SKILLS),
            placeholder="e.g. MATLAB, Verilog, Blender"
        )

        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")

    if submitted:
        # Validation
        errors = []
        if not name.strip():
            errors.append("Full Name is required.")
        if not email.strip() or "@" not in email:
            errors.append("A valid Email Address is required.")

        career = custom_career.strip() if career_goal_choice == "Other (specify below)" else career_goal_choice
        if not career:
            errors.append("Career Goal is required.")

        if errors:
            for e in errors:
                st.error(e)
            return

        custom_skills = [s.strip() for s in custom_skills_raw.split(",") if s.strip()]
        all_skills = list(dict.fromkeys(selected_skills + custom_skills))  # deduplicate, preserve order

        profile_data = {
            "name": name.strip(),
            "email": email.strip().lower(),
            "college": college.strip(),
            "branch": branch,
            "year": year,
            "current_skills": all_skills,
            "career_goal": career,
            "experience_level": exp_level,
        }

        save_profile(profile_data)
        session["profile"] = load_profile(profile_data["email"])
        session["email"] = profile_data["email"]

        st.success(f"✅ Profile saved! Welcome, **{name}**. Your goal: **{career}**")
        st.balloons()

    # Show current profile summary
    if session.get("profile"):
        p = session["profile"]
        st.markdown("---")
        st.markdown("#### 👤 Your Current Profile")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Name", p.get("name", "—"))
            st.metric("College", p.get("college", "—") or "—")
        with col2:
            st.metric("Branch", p.get("branch", "—"))
            st.metric("Year", p.get("year", "—"))
        with col3:
            st.metric("Career Goal", p.get("career_goal", "—"))
            st.metric("Experience", p.get("experience_level", "—"))

        skills = p.get("current_skills", [])
        if skills:
            st.markdown("**Skills:** " + "  ".join(f"`{s}`" for s in skills))
