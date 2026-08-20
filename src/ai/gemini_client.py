"""
src/ai/gemini_client.py
-----------------------
Reusable Google Gemini client for AI MentorX.

Uses the current official `google-genai` SDK (google.genai).

Key resolution order (first non-empty value wins):
  1. st.secrets["GEMINI_API_KEY"]   — Streamlit secrets (local .streamlit/secrets.toml
                                       or Streamlit Community Cloud secrets)
  2. GEMINI_API_KEY env var          — set via .env / shell / Docker

The key is NEVER hard-coded and NEVER exposed in the UI.
"""

from __future__ import annotations

import os
from typing import Optional

# ── Error sentinel returned when the AI call cannot complete ──────────────────
_ERR_PREFIX = "__AI_ERROR__"


def _error(msg: str) -> str:
    """Return a tagged error string so callers can detect failures."""
    return f"{_ERR_PREFIX}{msg}"


def is_error(text: str) -> bool:
    """True when the string is an AI error sentinel (not real content)."""
    return isinstance(text, str) and text.startswith(_ERR_PREFIX)


def error_message(text: str) -> str:
    """Strip the sentinel prefix and return the human-readable message."""
    return text[len(_ERR_PREFIX):]


# ── Key resolution ─────────────────────────────────────────────────────────────

def get_api_key() -> Optional[str]:
    """
    Resolve the Gemini API key without ever hard-coding it.

    Order:
      1. st.secrets["GEMINI_API_KEY"]
      2. GEMINI_API_KEY environment variable
    Returns None if neither is set.
    """
    # 1. Streamlit secrets (works locally via .streamlit/secrets.toml
    #    and on Streamlit Community Cloud via the secrets UI)
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key and key != "your_gemini_api_key_here":
            return key
    except Exception:
        pass  # st not yet initialised, or running outside Streamlit context

    # 2. Environment variable (.env loaded by python-dotenv in app.py)
    key = os.environ.get("GEMINI_API_KEY", "")
    if key and key != "your_gemini_api_key_here":
        return key

    return None


# ── Low-level generate call ───────────────────────────────────────────────────

_MODEL = "gemini-2.0-flash"   # fast, free-tier model


def generate(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.

    Returns a sentinel error string (detectable via is_error()) on failure
    so callers can decide how to surface it — never raises.

    Error cases handled:
      - Missing API key
      - Invalid / revoked API key  (google.genai.errors.ClientError 401/403)
      - Quota / rate-limit         (google.genai.errors.ClientError 429)
      - Network / server errors    (google.genai.errors.ServerError / OSError)
      - Empty model response
    """
    api_key = get_api_key()

    if not api_key:
        return _error(
            "GEMINI_API_KEY is not configured. "
            "Add it to `.streamlit/secrets.toml` (local) or Streamlit Cloud secrets."
        )

    try:
        from google import genai                        # google-genai SDK
        from google.genai import errors as genai_errors

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=_MODEL,
            contents=prompt,
        )

        text = ""
        if response and response.text:
            text = response.text.strip()

        if not text:
            return _error("The AI returned an empty response. Please try again.")

        return text

    # ── Auth errors ──────────────────────────────────────────────────────────
    except Exception as exc:
        exc_str = str(exc)
        exc_type = type(exc).__name__

        # Detect 401 / 403 — invalid or missing key
        if any(code in exc_str for code in ("401", "403", "API_KEY_INVALID",
                                             "PERMISSION_DENIED")):
            return _error(
                "Invalid or unauthorized GEMINI_API_KEY. "
                "Check your key at https://aistudio.google.com and update "
                "`GEMINI_API_KEY` in `.streamlit/secrets.toml`."
            )

        # Detect 429 — quota / rate limit
        if "429" in exc_str or "RESOURCE_EXHAUSTED" in exc_str:
            return _error(
                "Gemini API rate limit reached. "
                "Wait a moment and try again, or check your quota at "
                "https://aistudio.google.com."
            )

        # Network / connectivity
        if any(t in exc_type for t in ("ConnectionError", "TimeoutError",
                                        "OSError", "NetworkError")):
            return _error(
                f"Network error contacting Gemini API: {exc_str}. "
                "Check your internet connection and try again."
            )

        # Anything else
        return _error(f"Gemini API error ({exc_type}): {exc_str}")
