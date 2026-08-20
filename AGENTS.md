# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**AI MentorX** — Streamlit + Python + SQLite app in the `ai_mentorx/` subdirectory.
Run everything from inside `ai_mentorx/`:

```bash
cd ai_mentorx
pip install -r requirements.txt
streamlit run app.py
```

No test suite, no lint config. Syntax-check individual files with:
```bash
python -m py_compile <file.py>
```

## Critical path quirk

`app.py` calls `sys.path.insert(0, ROOT)` at startup, making `ai_mentorx/` itself the import root. All internal imports are therefore **relative to `ai_mentorx/`**, not the repo root:
- `from core.database import …`
- `from src.ai.gemini_client import …`
- `from pages.page_xyz import …`

Every page module also manually re-inserts its parent dir: `sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))` — needed because pages can be imported standalone.

## AI error pattern — mandatory

`src/ai/gemini_client.generate()` **never raises**. It returns a sentinel string prefixed with `__AI_ERROR__`. All callers in `core/ai_engine.py` must check `is_error(result)` before using the value. Skipping this check will silently pass error text to the UI as real AI output.

```python
from src.ai.gemini_client import generate, is_error, error_message
result = generate(prompt)
if is_error(result):
    return f"⚠️ {error_message(result)}"
```

## Gemini API key — resolution order

The key is resolved by `src/ai/gemini_client.get_api_key()` in this order:
1. `st.secrets["GEMINI_API_KEY"]` — from `.streamlit/secrets.toml` (local) or Streamlit Cloud secrets UI
2. `GEMINI_API_KEY` environment variable — from `.env` / shell

**Local dev:** put the key in `ai_mentorx/.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_key_here"
```
This file is in `.gitignore` and must never be committed.

**Model in use:** `gemini-2.0-flash` (set as `_MODEL` in `gemini_client.py`). Do not change to non-existent model names.

## Session state

All page `render(session)` functions receive `st.session_state` as `session` (a dict-like object). Pages read/write it directly — there is no separate state management layer.

## Database

`DB_PATH` defaults to `mentorx.db` in whichever directory the process starts from (usually `ai_mentorx/`). Override via env var `DB_PATH`. `init_db()` is idempotent — called once at app startup.

## Page module convention

Each page is a standalone module in `pages/` exporting exactly one function:
```python
def render(session: dict): ...
```
Register new pages in the `PAGES` dict in `app.py` only — no other wiring needed.
