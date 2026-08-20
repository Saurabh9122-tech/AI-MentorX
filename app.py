"""
app.py — AI MentorX Main Entry Point
Personalized Career, Skill-Gap & Interview Mentor for Students

AICTE / Edunet Foundation / IBM SkillsBuild Capstone Project
"""

import os
import sys
import streamlit as st

# ── Path setup so imports work from both `ai_mentorx/` and project root ───────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# ── Load .env if present (local dev) ─────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Gemini client (key resolution: st.secrets → env var) ─────────────────────
from src.ai.gemini_client import get_api_key

# ── DB initialisation ─────────────────────────────────────────────────────────
from core.database import init_db
init_db()

# ── Page imports ──────────────────────────────────────────────────────────────
from pages.page_home import render as home
from pages.page_profile import render as profile
from pages.page_career import render as career
from pages.page_skillgap import render as skillgap
from pages.page_roadmap import render as roadmap
from pages.page_assistant import render as assistant
from pages.page_quiz import render as quiz
from pages.page_interview import render as interview
from pages.page_projects import render as projects
from pages.page_progress import render as progress

# ── Streamlit page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI MentorX",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Hide default Streamlit header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        min-width: 240px;
    }
    section[data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
        padding: 4px 0;
    }

    /* Card-like containers */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Metric labels */
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }

    /* Button hover */
    .stButton > button:hover {
        border-color: #1a73e8;
        color: #1a73e8;
    }
</style>
""", unsafe_allow_html=True)


# ── Session state initialisation ──────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "🏠 Home",
        "profile": None,
        "email": None,
        "skill_gap": None,
        "roadmap": None,
        "chat_history": [],
        "quiz_questions": [],
        "quiz_answers": {},
        "quiz_submitted": False,
        "quiz_topic": "",
        "interview_questions_asked": [],
        "interview_current_q": None,
        "interview_evaluation": None,
        "projects": [],
        "progress_report": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session()
session = st.session_state  # convenience alias


# ── Sidebar Navigation ────────────────────────────────────────────────────────
PAGES = {
    "🏠 Home": home,
    "📋 Profile": profile,
    "🎯 Career Analysis": career,
    "🔍 Skill Gap": skillgap,
    "🗺️ Roadmap": roadmap,
    "🤖 AI Assistant": assistant,
    "📝 Quiz": quiz,
    "🎤 Mock Interview": interview,
    "💡 Projects": projects,
    "📊 Progress": progress,
}

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size:2rem;">🎓</div>
        <div style="font-size:1.2rem; font-weight:700; color:#ffffff;">AI MentorX</div>
        <div style="font-size:0.7rem; color:#aaa; margin-top:2px;">
            Powered by Google Gemini
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Profile quick-info
    p = session.get("profile")
    if p:
        st.markdown(f"""
        <div style="background:#ffffff15; border-radius:8px; padding:0.6rem;
                    margin-bottom:0.8rem; text-align:center;">
            <div style="font-size:0.85rem; color:#ffffff; font-weight:600;">
                👤 {p.get('name', '')}
            </div>
            <div style="font-size:0.75rem; color:#aaa;">
                {p.get('career_goal', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; color:#888; margin-bottom:4px;'>NAVIGATION</div>",
                unsafe_allow_html=True)

    selected = st.radio(
        "navigation",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(session.get("page", "🏠 Home")),
        label_visibility="collapsed",
    )

    session["page"] = selected

    st.markdown("---")

    # AI API Status indicator — uses the same resolution as the client
    if get_api_key():
        st.markdown("""
        <div style="background:#34a85320; border-radius:6px; padding:0.4rem 0.6rem;
                    font-size:0.78rem; color:#34a853;">
            🟢 AI Engine: Active
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#ea433520; border-radius:6px; padding:0.4rem 0.6rem;
                    font-size:0.78rem; color:#ea4335;">
            🔴 AI Key Missing — see README
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.65rem; color:#666; text-align:center;">
        AICTE · Edunet Foundation<br>IBM SkillsBuild · Capstone 2026
    </div>
    """, unsafe_allow_html=True)


# ── Render selected page ──────────────────────────────────────────────────────
PAGES[session["page"]](session)
