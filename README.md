# AI MentorX — Personalized Career, Skill-Gap & Interview Mentor for Students

> **AICTE · Edunet Foundation · IBM SkillsBuild Capstone Project 2025**

An AI-powered web application built with **Python + Streamlit + Google Gemini** that helps college students close skill gaps, prepare for technical careers, and practice for interviews — completely personalized to their profile.

---

## 🚀 Features

| Feature | What it does |
|---|---|
| 📋 **Student Profile** | Capture branch, year, skills, career goal |
| 🎯 **Career Analysis** | AI-generated role overview, salary, demand, progression |
| 🔍 **Skill Gap Analysis** | Identifies missing skills vs. career requirements |
| 🗺️ **Learning Roadmap** | Week-by-week plan with free resources |
| 🤖 **AI Learning Assistant** | Chat with an AI mentor personalized to your goal |
| 📝 **Adaptive Quiz** | AI-generated MCQ quizzes on any topic |
| 🎤 **Mock Interview** | Realistic AI interview questions + scored feedback |
| 💡 **Project Recommendations** | Portfolio project ideas matched to your level |
| 📊 **Progress Dashboard** | Track quizzes, interviews, activities, and get AI feedback |

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| Frontend / UI | Streamlit ≥ 1.35 |
| AI / LLM | Google Gemini 2.0 Flash (`google-genai` SDK) |
| Gemini client | `src/ai/gemini_client.py` (swappable module) |
| Database | SQLite (local, zero-config) |
| Language | Python 3.10+ |
| Deployment | Streamlit Community Cloud (free) |

---

## 📋 Prerequisites

- Python 3.10 or higher
- A Google Gemini API key (free — instructions below)

---

## 🔑 Step 1 — Create a Free Gemini API Key

1. Go to **[https://aistudio.google.com](https://aistudio.google.com)**
2. Sign in with your Google account
3. Click **"Get API Key"** in the top-left menu
4. Click **"Create API key"** → choose or create a Google Cloud project
5. Copy the generated key — it looks like `AIzaSy…` or `AQ.Ab8…`

> The free tier includes generous daily quotas and requires no payment method.

---

## 🛠️ Step 2 — Configure the Key for Local Development

Create `.streamlit/secrets.toml` in the project folder (this file is already in `.gitignore` and will **never** be committed to Git):

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

Streamlit reads this file automatically when you run `streamlit run app.py`.

> **Alternative:** You can also set the environment variable directly:
> ```bash
> export GEMINI_API_KEY="your_actual_gemini_api_key_here"   # macOS / Linux
> set GEMINI_API_KEY=your_actual_gemini_api_key_here         # Windows CMD
> $env:GEMINI_API_KEY="your_actual_gemini_api_key_here"      # PowerShell
> ```
> Or add it to a `.env` file — `python-dotenv` will load it automatically.

---

## ▶️ Step 3 — Install & Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-mentorx.git
cd ai-mentorx

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

The sidebar shows **🟢 AI Engine: Active** when the key is correctly configured.

---

## 🌐 Step 4 — Deploy on Streamlit Community Cloud (Free)

### 4a. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AI MentorX"
git remote add origin https://github.com/YOUR_USERNAME/ai-mentorx.git
git push -u origin main
```

> Make sure `.streamlit/secrets.toml` is **not** in the commit — it is excluded by `.gitignore`.

### 4b. Create the Streamlit app

1. Go to **[https://share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub → click **"New app"**
3. Select your repository and branch
4. Set **Main file path** to `app.py`

### 4c. Add the API key as a secret

1. In the app settings page, expand **"Advanced settings"**
2. Paste the following into the **Secrets** text box:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

3. Click **"Save"**

### 4d. Deploy

Click **"Deploy"** — the app will be live at `https://your-app.streamlit.app` in about 60 seconds.

> **Note:** Streamlit Community Cloud does not persist the SQLite database across re-deploys.
> For permanent storage in production, set `DB_PATH` in secrets to a writable path,
> or migrate to a hosted database (e.g., Supabase free tier).

---

## 📁 Project Structure

```
ai-mentorx/
├── app.py                        # Main Streamlit entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .streamlit/
│   ├── config.toml               # Streamlit theme / server config
│   └── secrets.toml              # Local secrets (NEVER commit this)
├── src/
│   └── ai/
│       └── gemini_client.py      # google-genai client (key resolution + error handling)
├── core/
│   ├── ai_engine.py              # All AI feature functions (prompts)
│   └── database.py               # SQLite persistence layer
└── pages/
    ├── page_home.py
    ├── page_profile.py
    ├── page_career.py
    ├── page_skillgap.py
    ├── page_roadmap.py
    ├── page_assistant.py
    ├── page_quiz.py
    ├── page_interview.py
    ├── page_projects.py
    └── page_progress.py
```

---

## 🔌 AI Key Resolution Order

The Gemini client (`src/ai/gemini_client.py`) resolves the API key in this order:

1. **`st.secrets["GEMINI_API_KEY"]`** — reads from `.streamlit/secrets.toml` locally, or from the Streamlit Cloud secrets UI in production
2. **`GEMINI_API_KEY` environment variable** — set via `.env` file, shell export, or Docker

The key is **never hard-coded** and **never shown in the UI**.

---

## ⚠️ Error Handling

The app handles all API failure modes gracefully:

| Condition | What the user sees |
|---|---|
| Key not configured | Clear message with setup instructions |
| Invalid / revoked key | Descriptive error with link to AI Studio |
| Rate limit (429) | Message to wait and retry |
| Network error | Message to check internet connection |
| Empty AI response | Message to try again |

All AI features degrade gracefully — the rest of the app continues to work.

---

## 📜 License

MIT License — free to use, modify, and distribute for educational purposes.

---

*Built for the AICTE / Edunet Foundation / IBM SkillsBuild Internship Program*
