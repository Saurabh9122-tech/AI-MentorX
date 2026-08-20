"""
core/ai_engine.py — AI feature functions for AI MentorX
All prompts live here; the actual API call is delegated to
src/ai/gemini_client.generate() so the provider is swappable.
"""

from __future__ import annotations

import json
import re
import sys
import os
from typing import Any

# Make sure src/ is importable regardless of cwd
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from src.ai.gemini_client import generate, is_error


# ── JSON helpers ──────────────────────────────────────────────────────────────

def _clean_json(text: str) -> str:
    """Strip markdown fences that LLMs sometimes add around JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_json_response(text: str, fallback: Any) -> Any:
    """
    Try to parse the AI response as JSON.
    Falls back to `fallback` if parsing fails.
    If the text is an AI error sentinel it is returned directly so the
    calling page can decide how to display it.
    """
    if is_error(text):
        return fallback  # callers receive the fallback; error shown by page via is_error check

    cleaned = _clean_json(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return fallback


def _ask_ai(prompt: str) -> str:
    """
    Single call-site for all AI requests.
    Returns the raw text (may be an error sentinel — callers use is_error() to detect).
    """
    return generate(prompt)


# ── 1. Career Analysis ────────────────────────────────────────────────────────

def analyze_career(career_goal: str, branch: str, current_skills: list[str]) -> str:
    """
    Returns a markdown-formatted career overview.
    On error returns a user-friendly error string.
    """
    skills_str = ", ".join(current_skills) if current_skills else "none listed"
    prompt = f"""
You are a career counselor for college students in India.
The student's branch: {branch}
Their target career: {career_goal}
Skills they already have: {skills_str}

Write a concise, honest career overview in Markdown covering:
1. **What the Role Involves** (3-4 sentences)
2. **Industry Demand in India & Globally** (2-3 sentences)
3. **Typical Salary Range** (entry to senior, INR and USD)
4. **Career Progression Path** (bullet list: fresher → 5 years → 10 years)
5. **Key Companies Hiring** (5-7 company names)

Be factual. Do not fabricate numbers. Use "approximately" where precise figures are uncertain.
"""
    result = _ask_ai(prompt)
    if is_error(result):
        from src.ai.gemini_client import error_message
        return f"⚠️ **AI Unavailable:** {error_message(result)}"
    return result


# ── 2. Skill Gap Analysis ─────────────────────────────────────────────────────

def analyze_skill_gap(career_goal: str, current_skills: list[str],
                      branch: str, year: int) -> dict:
    """
    Returns a dict with keys: required_skills, gaps, strengths, priority_order.
    Returns a sensible fallback dict on error.
    """
    skills_str = ", ".join(current_skills) if current_skills else "none"
    prompt = f"""
You are a technical skills advisor.
Student info: Branch={branch}, Year={year}
Career target: {career_goal}
Current skills: {skills_str}

Return ONLY valid JSON (no markdown fences, no explanation) in this exact shape:
{{
  "required_skills": ["skill1", "skill2", ...],
  "gaps": ["missing_skill1", "missing_skill2", ...],
  "strengths": ["already_known_skill1", ...],
  "priority_order": ["most_urgent_gap_first", ...]
}}

List 8-12 required skills. Gaps = required minus current skills. Priority = order to learn gaps.
"""
    fallback = {
        "required_skills": ["Python", "SQL", "Data Analysis", "Machine Learning",
                            "Statistics", "Communication"],
        "gaps": ["Machine Learning", "Statistics"],
        "strengths": ["Python", "SQL"],
        "priority_order": ["Statistics", "Machine Learning"],
        "_error": None,
    }
    raw = _ask_ai(prompt)
    if is_error(raw):
        from src.ai.gemini_client import error_message
        fallback["_error"] = error_message(raw)
        return fallback
    return _parse_json_response(raw, fallback)


# ── 3. Roadmap Generation ─────────────────────────────────────────────────────

def generate_roadmap(career_goal: str, gaps: list[str], year: int) -> list[dict]:
    """
    Returns a list of roadmap phase dicts.
    Returns a single-entry fallback list on error.
    """
    gaps_str = ", ".join(gaps) if gaps else "general upskilling"
    months_available = max(1, (4 - year) * 6)
    prompt = f"""
You are a learning path designer.
Career goal: {career_goal}
Skills to learn (in priority order): {gaps_str}
Approximate time available: {months_available} months

Return ONLY a valid JSON array (no markdown fences) of learning steps:
[
  {{
    "phase": "Phase 1 – Foundations",
    "duration": "Weeks 1-4",
    "topic": "Topic name",
    "description": "What to learn and why",
    "resources": ["Free resource 1 (platform name)", "Free resource 2"],
    "milestone": "What you can do after this phase"
  }},
  ...
]

Include 5-7 phases. Use only free resources (Coursera free audit, YouTube, freeCodeCamp, Kaggle, etc.).
"""
    fallback = [
        {
            "phase": "Phase 1 – Foundations",
            "duration": "Weeks 1-4",
            "topic": gaps[0] if gaps else "Core Fundamentals",
            "description": "Build foundational knowledge.",
            "resources": ["YouTube tutorials", "freeCodeCamp"],
            "milestone": "Understand core concepts",
        }
    ]
    raw = _ask_ai(prompt)
    if is_error(raw):
        return fallback
    result = _parse_json_response(raw, fallback)
    return result if isinstance(result, list) else fallback


# ── 4. Learning Assistant ─────────────────────────────────────────────────────

def ask_learning_assistant(question: str, career_goal: str,
                           current_skills: list[str], chat_history: list[dict]) -> str:
    """
    Conversational AI tutor.
    chat_history = [{"role": "user"|"ai", "text": "..."}]
    Returns a user-facing error string if the API is unavailable.
    """
    history_str = ""
    for msg in chat_history[-6:]:
        role = "Student" if msg["role"] == "user" else "Mentor"
        history_str += f"{role}: {msg['text']}\n"

    skills_str = ", ".join(current_skills) if current_skills else "beginner"
    prompt = f"""
You are AI MentorX, a friendly and knowledgeable learning mentor for students
targeting a career in: {career_goal}.
Student's current skill level: {skills_str}

Recent conversation:
{history_str}
Student: {question}

Provide a clear, helpful, encouraging answer. Use examples. Keep it concise (under 300 words).
If the question is outside career/tech learning, gently redirect.
"""
    result = _ask_ai(prompt)
    if is_error(result):
        from src.ai.gemini_client import error_message
        return f"⚠️ **AI Unavailable:** {error_message(result)}"
    return result


# ── 5. Quiz Generation ────────────────────────────────────────────────────────

def generate_quiz(topic: str, difficulty: str, num_questions: int = 5) -> list[dict]:
    """
    Returns a list of MCQ dicts.
    Returns a minimal fallback list on error.
    """
    prompt = f"""
Generate exactly {num_questions} multiple-choice questions about "{topic}"
at {difficulty} difficulty level for a college student.

Return ONLY a valid JSON array (no markdown fences, no extra text):
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A",
    "explanation": "Brief explanation of why this is correct."
  }},
  ...
]

Make sure the "answer" field exactly matches one of the "options" strings.
"""
    fallback = [
        {
            "question": f"What is a fundamental concept in {topic}?",
            "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
            "answer": "Concept A",
            "explanation": "Concept A is the foundational principle.",
        }
    ]
    raw = _ask_ai(prompt)
    if is_error(raw):
        return fallback
    result = _parse_json_response(raw, fallback)
    return result if isinstance(result, list) else fallback


# ── 6. Mock Interview ─────────────────────────────────────────────────────────

def get_interview_question(career_goal: str, round_type: str,
                           previous_questions: list[str]) -> str:
    """
    Generate a single interview question.
    Returns a user-facing error string if the API is unavailable.
    """
    prev_str = "\n".join(f"- {q}" for q in previous_questions[-5:]) if previous_questions else "None"
    prompt = f"""
You are an interviewer at a top tech company.
Role being interviewed for: {career_goal}
Interview round type: {round_type}
Questions already asked:
{prev_str}

Generate ONE new interview question that is different from the above.
Return ONLY the question text, nothing else.
"""
    result = _ask_ai(prompt)
    if is_error(result):
        from src.ai.gemini_client import error_message
        return f"⚠️ Could not generate question: {error_message(result)}"
    return result.strip()


def evaluate_interview_answer(question: str, answer: str, career_goal: str) -> dict:
    """
    Evaluate a candidate's answer.
    Returns {"score": int, "feedback": str, "improved_answer": str}.
    Returns a sensible fallback dict on error.
    """
    prompt = f"""
You are a senior interviewer evaluating a candidate for: {career_goal}

Interview Question: {question}

Candidate's Answer: {answer}

Return ONLY valid JSON (no markdown fences):
{{
  "score": <integer 1-10>,
  "feedback": "Specific, constructive feedback on what was good and what to improve",
  "improved_answer": "A concise example of a stronger answer (2-3 sentences)"
}}

Be fair, specific, and encouraging. Score 1=poor, 5=average, 10=excellent.
"""
    fallback = {
        "score": 5,
        "feedback": "Your answer covered the basics. Consider adding specific examples.",
        "improved_answer": "A stronger answer would include concrete examples from your experience.",
    }
    raw = _ask_ai(prompt)
    if is_error(raw):
        from src.ai.gemini_client import error_message
        fallback["feedback"] = f"⚠️ AI Unavailable: {error_message(raw)}"
        return fallback
    return _parse_json_response(raw, fallback)


# ── 7. Project Recommendations ────────────────────────────────────────────────

def recommend_projects(career_goal: str, current_skills: list[str],
                       gaps: list[str]) -> list[dict]:
    """
    Returns a list of 5 project idea dicts.
    Returns a single-entry fallback list on error.
    """
    skills_str = ", ".join(current_skills) if current_skills else "basic"
    gaps_str = ", ".join(gaps[:5]) if gaps else "general"
    prompt = f"""
You are a project mentor for students targeting: {career_goal}
Student's current skills: {skills_str}
Skills they are learning: {gaps_str}

Suggest exactly 5 hands-on projects that will help build their portfolio.
Return ONLY a valid JSON array (no markdown fences):
[
  {{
    "title": "Project Title",
    "description": "2-3 sentence project description",
    "skills_used": ["skill1", "skill2"],
    "difficulty": "Beginner|Intermediate|Advanced",
    "estimated_time": "e.g. 1 week",
    "github_idea": "Brief idea for a GitHub repo name and structure"
  }},
  ...
]
"""
    fallback = [
        {
            "title": f"Portfolio Project for {career_goal}",
            "description": "Build a foundational project to demonstrate your skills.",
            "skills_used": current_skills[:3] if current_skills else ["Python"],
            "difficulty": "Beginner",
            "estimated_time": "1-2 weeks",
            "github_idea": "portfolio-project-v1",
        }
    ]
    raw = _ask_ai(prompt)
    if is_error(raw):
        return fallback
    result = _parse_json_response(raw, fallback)
    return result if isinstance(result, list) else fallback


# ── 8. Overall Feedback ───────────────────────────────────────────────────────

def generate_overall_feedback(profile: dict, quiz_history: list,
                              interview_history: list) -> str:
    """
    Generate a personalized progress report.
    Returns a user-facing error string if the API is unavailable.
    """
    avg_quiz = 0.0
    if quiz_history:
        avg_quiz = sum(r["score"] / max(r["total"], 1) * 100
                       for r in quiz_history) / len(quiz_history)

    avg_interview = 0.0
    if interview_history:
        scores = [r.get("score", 0) for r in interview_history if r.get("score")]
        avg_interview = sum(scores) / len(scores) if scores else 0.0

    prompt = f"""
You are an academic advisor reviewing a student's AI MentorX progress.

Student: {profile.get('name', 'Student')}
Career Goal: {profile.get('career_goal', 'Not set')}
Current Skills: {', '.join(profile.get('current_skills', []))}
Quizzes taken: {len(quiz_history)}, Average score: {avg_quiz:.1f}%
Mock interview rounds: {len(interview_history)}, Average score: {avg_interview:.1f}/10

Write a personalized, encouraging 200-word progress report in Markdown covering:
1. **What's Going Well**
2. **Areas to Focus On**
3. **Top 3 Recommended Next Actions**

Be specific, realistic, and motivating. Never fabricate results.
"""
    result = _ask_ai(prompt)
    if is_error(result):
        from src.ai.gemini_client import error_message
        return f"⚠️ **AI Unavailable:** {error_message(result)}"
    return result
