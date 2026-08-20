"""
database.py — SQLite persistence layer for AI MentorX
All student data, progress, quiz results, and interview logs are stored here.
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "mentorx.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            college TEXT,
            branch TEXT,
            year INTEGER,
            current_skills TEXT,       -- JSON list
            career_goal TEXT,
            experience_level TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS skill_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            career_goal TEXT,
            gaps TEXT,                 -- JSON list
            roadmap TEXT,              -- JSON list of steps
            analyzed_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            details TEXT,              -- JSON list of Q&A results
            taken_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS interview_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            career_goal TEXT,
            question TEXT,
            answer TEXT,
            feedback TEXT,
            score INTEGER,
            logged_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            action TEXT,
            detail TEXT,
            logged_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# ── Profile ──────────────────────────────────────────────────────────────────

def save_profile(data: dict):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().isoformat()
    skills_json = json.dumps(data.get("current_skills", []))
    c.execute("""
        INSERT INTO profiles (name, email, college, branch, year, current_skills,
                              career_goal, experience_level, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            name=excluded.name, college=excluded.college, branch=excluded.branch,
            year=excluded.year, current_skills=excluded.current_skills,
            career_goal=excluded.career_goal, experience_level=excluded.experience_level,
            updated_at=excluded.updated_at
    """, (
        data["name"], data["email"], data.get("college", ""),
        data.get("branch", ""), data.get("year", 1), skills_json,
        data.get("career_goal", ""), data.get("experience_level", "Beginner"), now, now
    ))
    conn.commit()
    conn.close()
    log_progress(data["email"], "profile_updated", "Profile saved/updated")


def load_profile(email: str) -> dict | None:
    conn = get_conn()
    c = conn.cursor()
    row = c.execute("SELECT * FROM profiles WHERE email = ?", (email,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["current_skills"] = json.loads(d.get("current_skills") or "[]")
        return d
    return None


# ── Skill Gap & Roadmap ──────────────────────────────────────────────────────

def save_skill_gap(email: str, career_goal: str, gaps: list, roadmap: list):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("""
        INSERT INTO skill_gaps (email, career_goal, gaps, roadmap, analyzed_at)
        VALUES (?, ?, ?, ?, ?)
    """, (email, career_goal, json.dumps(gaps), json.dumps(roadmap), now))
    conn.commit()
    conn.close()
    log_progress(email, "skill_gap_analyzed", f"Gap analysis for {career_goal}")


def load_latest_skill_gap(email: str) -> dict | None:
    conn = get_conn()
    c = conn.cursor()
    row = c.execute(
        "SELECT * FROM skill_gaps WHERE email = ? ORDER BY id DESC LIMIT 1", (email,)
    ).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["gaps"] = json.loads(d.get("gaps") or "[]")
        d["roadmap"] = json.loads(d.get("roadmap") or "[]")
        return d
    return None


# ── Quiz ─────────────────────────────────────────────────────────────────────

def save_quiz_result(email: str, topic: str, score: int, total: int, details: list):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("""
        INSERT INTO quiz_results (email, topic, score, total, details, taken_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email, topic, score, total, json.dumps(details), now))
    conn.commit()
    conn.close()
    log_progress(email, "quiz_completed", f"{topic}: {score}/{total}")


def load_quiz_history(email: str) -> list:
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute(
        "SELECT * FROM quiz_results WHERE email = ? ORDER BY id DESC LIMIT 20", (email,)
    ).fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["details"] = json.loads(d.get("details") or "[]")
        result.append(d)
    return result


# ── Interview ────────────────────────────────────────────────────────────────

def save_interview_log(email: str, career_goal: str, question: str,
                       answer: str, feedback: str, score: int):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("""
        INSERT INTO interview_logs (email, career_goal, question, answer, feedback, score, logged_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (email, career_goal, question, answer, feedback, score, now))
    conn.commit()
    conn.close()
    log_progress(email, "interview_question", f"Score: {score}/10")


def load_interview_history(email: str) -> list:
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute(
        "SELECT * FROM interview_logs WHERE email = ? ORDER BY id DESC LIMIT 20", (email,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── Progress ─────────────────────────────────────────────────────────────────

def log_progress(email: str, action: str, detail: str):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "INSERT INTO progress (email, action, detail, logged_at) VALUES (?, ?, ?, ?)",
        (email, action, detail, now)
    )
    conn.commit()
    conn.close()


def load_progress(email: str) -> list:
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute(
        "SELECT * FROM progress WHERE email = ? ORDER BY id DESC LIMIT 50", (email,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
