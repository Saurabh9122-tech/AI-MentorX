# 🎓 AI MentorX — Personalized Career, Skill-Gap & Interview Mentor

> **AICTE · Edunet Foundation · IBM SkillsBuild AI Internship Capstone Project 2026**

AI MentorX is an AI-powered career and learning mentor designed for college students, fresh graduates, and entry-level job seekers.

The application helps students understand their career requirements, identify skill gaps, create personalized learning roadmaps, learn with an AI assistant, practice through quizzes and mock interviews, receive AI-generated feedback, and discover suitable portfolio projects.

---

## 🎯 Problem Statement

Students often struggle to understand:

- Which skills are required for their desired career
- Which skills they already have
- Which skills they are missing
- What they should learn next
- How to prepare for technical and HR interviews
- Which projects can improve their portfolio

Many existing learning platforms provide generic recommendations that do not consider a student's current skills, academic background, career goal, experience level, or available study time.

Therefore, there is a need for a personalized AI-based mentoring system that can guide students throughout their career preparation journey.

---

## 💡 Proposed Solution

AI MentorX provides an integrated AI mentoring platform that analyzes a student's profile and career goal to generate personalized recommendations.

The system combines:

- Student Profile
- Career Analysis
- Skill-Gap Analysis
- Personalized Learning Roadmap
- AI Learning Assistant
- AI Quiz Generator
- AI Mock Interview
- AI Feedback
- Project Recommendations
- Progress Dashboard

The application uses the **Google Gemini API** to provide AI-powered analysis, explanations, recommendations, question generation, and feedback.

> **Important:** AI MentorX does not train a machine-learning model from scratch. It uses a Large Language Model (LLM) through the Gemini API along with application logic, structured prompts, and student profile information to generate personalized results.

---

# 🚀 Key Features

## 📋 1. Student Profile

Students can provide information such as:

- Name
- Degree
- Department / Branch
- Year / Semester
- Technical skills
- Programming languages
- Soft skills
- Certifications
- Projects
- Preferred career role
- Experience level
- Weekly learning time

This information is used to personalize the application's recommendations.

---

## 🎯 2. Career Analysis

The system analyzes the student's selected career goal and provides information about:

- Required skills
- Important technologies
- Preparation areas
- Career expectations
- Learning priorities
- Recommended preparation strategy

Example career goals include:

- Java Developer
- Python Developer
- Full Stack Developer
- Data Analyst
- AI/ML Engineer
- Software Engineer
- Cloud Engineer

---

## 🔍 3. AI Skill-Gap Analysis

The system compares the student's current skills with the skills generally required for the selected career.

It identifies:

- Existing strengths
- Missing skills
- Skill priorities
- Beginner/intermediate/advanced areas
- Recommended learning order
- Areas requiring improvement

This helps students understand exactly what they should focus on.

---

## 🗺️ 4. Personalized Learning Roadmap

AI MentorX generates a customized learning roadmap based on:

- Current skill level
- Target career
- Existing knowledge
- Available weekly study time
- Identified skill gaps

The roadmap can contain:

- Weekly objectives
- Topics to learn
- Practice activities
- Mini-project suggestions
- Revision activities
- Assessment checkpoints

The goal is to provide a learning plan that is personalized rather than identical for every student.

---

## 🤖 5. AI Learning Assistant

The AI Learning Assistant acts as a personalized study mentor.

Students can use it to:

- Understand technical concepts
- Ask follow-up questions
- Simplify difficult topics
- Get examples
- Understand programming concepts
- Receive career-focused explanations

The assistant can adapt explanations to the student's learning requirements.

---

## 📝 6. AI Quiz Generator

The application can generate quizzes based on a selected topic.

Supported question types include:

- Multiple Choice Questions
- True/False Questions
- Scenario-based Questions

After completing a quiz, the system can provide:

- Quiz score
- Answer evaluation
- Explanations
- Weak-topic identification
- Revision recommendations

---

## 🎤 7. AI Mock Interview

AI MentorX provides an interactive interview practice environment.

Supported modes:

- Technical Interview
- HR Interview
- Mixed Interview

The AI asks interview questions and evaluates the student's responses.

The feedback can include:

- Overall performance
- Technical knowledge
- Answer quality
- Communication
- Strengths
- Weaknesses
- Improvement suggestions
- Recommended preparation topics

---

## 💡 8. AI Project Recommendations

The system recommends portfolio projects based on the student's:

- Career goal
- Existing skills
- Skill gaps
- Experience level

Each project recommendation can include:

- Project title
- Problem statement
- Technologies
- Main modules
- Difficulty level
- Skills learned
- Expected learning outcome

This helps students build projects that are relevant to their career goals.

---

## 📊 9. Progress Dashboard

The Progress Dashboard provides an overview of the student's preparation.

It can display:

- Current career goal
- Completed skills
- Remaining skills
- Quiz performance
- Interview performance
- Roadmap progress
- Recommended next actions

---

# 🔄 Application Workflow

```text
Student Profile
       ↓
Career Goal
       ↓
Career Analysis
       ↓
Skill-Gap Analysis
       ↓
Personalized Roadmap
       ↓
AI Learning Assistant
       ↓
AI Quiz
       ↓
Mock Interview
       ↓
AI Feedback
       ↓
Project Recommendations
       ↓
Progress Dashboard
       ↓
Next Learning Recommendation
```

---

# 🧠 AI Capabilities

The application uses an LLM-based AI architecture for:

- Career analysis
- Skill-gap identification
- Personalized learning recommendations
- Technical explanations
- Quiz generation
- Interview question generation
- Interview evaluation
- Project recommendations
- Progress-based recommendations

### AI Approach

The application does not train an ML model from scratch.

Instead, it uses:

```text
Student Information
        ↓
Application Logic
        ↓
Structured Prompt
        ↓
Google Gemini API
        ↓
AI Generated Response
        ↓
Application Processing
        ↓
Personalized Result
```

The application uses prompt engineering and structured inputs to generate useful responses based on the student's context.

---

# 🏗️ System Architecture

```text
                         ┌───────────────────┐
                         │      Student      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Streamlit UI    │
                         │      app.py       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Feature Pages   │
                         │      pages/       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     AI Engine     │
                         │ core/ai_engine.py │
                         └───────┬───┬───────┘
                                 │   │
                     ┌───────────┘   └────────────┐
                     ▼                            ▼
           ┌──────────────────┐        ┌──────────────────┐
           │ SQLite Database  │        │  Gemini Client   │
           │ core/database.py │        │ gemini_client.py │
           └──────────────────┘        └────────┬─────────┘
                                                │
                                                ▼
                                      ┌──────────────────┐
                                      │ Google Gemini API │
                                      └──────────────────┘
```

---

# 🤖 AI Component Architecture

The AI functionality is divided into logical capabilities:

```text
                  Google Gemini API
                         │
                         ▼
                Gemini Client Layer
                         │
                         ▼
                    AI Engine
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
 Career Analysis    Skill Gap         Roadmap
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
        Assistant      Quiz       Interview
            │            │            │
            └────────────┼────────────┘
                         │
                         ▼
               Recommendations
                         │
                         ▼
                 Progress Tracking
```

These are **logical AI capabilities** implemented through application functions and prompts. They do not necessarily represent separate autonomous AI models.

---

# 🏗️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend / UI | Streamlit |
| AI / LLM | Google Gemini API |
| AI SDK | Google GenAI SDK |
| Database | SQLite |
| Environment Management | Python dotenv / Streamlit Secrets |
| Version Control | Git |
| Repository | GitHub |
| Deployment | Streamlit Community Cloud |

---

# 📁 Project Structure

```text
AI-MentorX/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   └── ai/
│       └── gemini_client.py
│
├── core/
│   ├── ai_engine.py
│   └── database.py
│
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

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Saurabh9122-tech/AI-MentorX.git
cd AI-MentorX
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Configuration

AI MentorX requires a Google Gemini API key for AI-powered features.

For local development, create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Alternatively, an environment variable can be used:

```text
GEMINI_API_KEY
```

### ⚠️ Security

Never commit your actual API key to GitHub.

Your `.gitignore` should contain:

```text
.streamlit/secrets.toml
.env
.env.*
__pycache__/
*.pyc
*.db
venv/
```

The API key should never be hard-coded inside Python source files.

---

# ▶️ Run the Application

Start the application using:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

When the Gemini API key is configured correctly, the application displays:

```text
🟢 AI Engine: Active
```

---

# 🌐 Deployment

AI MentorX can be deployed using **Streamlit Community Cloud**.

## Deployment Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Sign in using GitHub.
4. Create a new application.
5. Select the `AI-MentorX` repository.
6. Select the `main` branch.
7. Set the main file to:

```text
app.py
```

8. Add the Gemini API key through Streamlit Secrets:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

9. Deploy the application.

After successful deployment, Streamlit provides a public application URL.

---

# 🔐 Security & Privacy

The project follows basic security practices:

- API keys are not hard-coded.
- Secrets are excluded from Git.
- Environment variables can be used for sensitive configuration.
- User inputs are processed through application logic.
- AI responses are handled through the AI layer.
- Sensitive configuration is separated from application source code.

For production-scale deployment, additional security measures should be implemented, including:

- User authentication
- Authorization
- Database security
- Rate limiting
- Input sanitization
- Privacy controls
- Secure cloud storage

---

# ⚠️ Limitations

AI MentorX is an educational AI capstone project.

Important limitations include:

- AI-generated information may contain inaccuracies.
- Career requirements can change over time.
- Students should independently verify important career information.
- AI recommendations should not be treated as guaranteed career outcomes.
- SQLite is suitable for local/demo usage but is not ideal for a large multi-user production system.
- Gemini API availability and quotas depend on the current Google API plan and service limits.
- AI responses depend on the quality and completeness of user-provided information.

---

# 🔮 Future Scope

Future versions could include:

- 👤 User authentication
- ☁️ Cloud database
- 📄 Resume PDF upload and analysis
- 💼 Job-description analysis
- 🔎 Real-time job-market analysis
- 🎙️ Voice-based mock interviews
- 🌐 Multilingual AI mentoring
- 📱 Mobile application
- 📈 Advanced learning analytics
- 🧠 Advanced personalized recommendation systems
- 🔗 Integration with job and professional platforms
- 🏢 Company-specific interview preparation
- 📚 Integration with external learning resources
- 📄 Automated resume improvement
- 🎯 Personalized placement preparation

---

# 🧪 Testing

The application should be tested for:

- Valid student profiles
- Invalid student profiles
- Missing API keys
- Invalid API keys
- Gemini API failures
- Network/API errors
- Empty AI responses
- Quiz generation
- Quiz evaluation
- Interview question generation
- Interview evaluation
- Database operations
- Page navigation
- Session-state handling
- Responsive UI behavior

---

# 📚 Project Documentation

The project documentation covers:

- Problem Statement
- Proposed Solution
- System Architecture
- Technology Stack
- AI Approach
- Application Workflow
- AI Capabilities
- Results
- Limitations
- Future Scope
- Testing
- Deployment

---

# 📊 Expected Results

The expected outcome of AI MentorX is to provide students with a single platform where they can:

```text
Understand Career Goal
        ↓
Identify Required Skills
        ↓
Find Personal Skill Gaps
        ↓
Create Learning Roadmap
        ↓
Learn with AI
        ↓
Test Knowledge
        ↓
Practice Interviews
        ↓
Receive Feedback
        ↓
Build Relevant Projects
        ↓
Track Progress
```

The system aims to make career preparation more structured, personalized, and accessible.

---

# 👨‍💻 Developed By

**Saurabh Kumar**

BCA Student  
**Uttaranchal University**

### Internship

**Edunet Foundation · AICTE · IBM SkillsBuild**

### Project

**AI MentorX — Personalized Career, Skill-Gap & Interview Mentor**

### Internship Type

**6-Week Artificial Intelligence Internship**

---

# 🏆 Project Purpose

This project was developed as a capstone project during the:

**Edunet Foundation AI Internship leveraging the IBM SkillsBuild learning ecosystem.**

The project demonstrates the practical use of:

- Generative AI
- Large Language Models
- Prompt Engineering
- Python
- Streamlit
- API Integration
- Database Management
- AI-powered personalization
- Git and GitHub
- Cloud Deployment

---

# 📜 License

This project is licensed under the **MIT License**.

---

# ⭐ Acknowledgement

Special thanks to:

- **Edunet Foundation**
- **AICTE**
- **IBM SkillsBuild**
- **Google Gemini API**
- **Uttaranchal University**

for providing the learning ecosystem and opportunity to develop this AI-focused capstone project.

---

> **AI MentorX — Helping students understand what to learn, how to learn, and how to prepare for their career.** 🎓🤖
