Samvaad Saathi – AI Interview Coach 

Samvaad Saathi is an AI-powered interview simulation and coaching platform.
It helps students and professionals practice real interviews, get feedback on their answers, and improve communication skills.

The backend is built with FastAPI + PostgreSQL, powered by LLM-based analysis for question generation, audio transcription, and performance evaluation.

1. Directory Structure
.
├── app/
│   ├── main.py              # FastAPI entrypoint
│   │
│   ├── users/               # User registration & profile management
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── services.py      # Business logic
│   │   └── routes.py        # API routes
│   │
│   ├── sessions/            # Login / Logout handling
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── routes.py
│   │
│   ├── interviews/          # Interview workflow (create, start questions, answers)
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── routes.py
│   │
│   ├── reports/             # Final performance report generation
│   │   ├── models.py
|   |   ├── schemas.py
│   │   ├── services.py
│   │   └── routes.py
│   │
│   ├── core/                # Shared utilities
│   │   ├── llm.py           # OpenAI calls
│   │   ├── analysis_sqs.py  # Analysis AWS SQS integration
│   │   ├── report_sqs.py    # Report AWS SQS integration
│   ├── prompts/             # All system / user prompts for LLMs
|   |   └── prompts.py
│   │
│   ├── workers/             # Background workers for async processing
│   │   ├── transcription_worker.py
│   │   └── analysis_worker.py
│   │
│   │
│   └── database.py          # Database session + engine
│
├── requirements.txt         # Dependencies
├── .env                     # Env variable template
└── README.md                # ← You are here


🛠 What Each Module Does  

| Path | Purpose |
|------|---------|
| app/main.py | FastAPI entrypoint; mounts routes from all services. |
| users/ | Manages user sign-up & profile. |
| sessions/ | Handles login/logout & session tokens. |
| interviews/ | Core interview workflow – create session, generate questions, record answers. |
| reports/ | Generates summary reports (feedback, scores, improvement tips). |
| core/llm.py | Wrapper around LLM APIs (OpenAI, etc.). |
| core/sqs.py | Queue handling (async processing with workers). |
| workers/ | Long-running background tasks – transcription, analysis. |
| prompts/ | All reusable LLM prompt templates. |


2. High-Level Flow  

1.Sign Up & Login
   - User creates account (via email or Google).  
   - Session service issues token for authentication.  

2.Interview Session Creation  
   - User selects job role / interview type.  
   - Backend creates an `Interview` object and starts an interview attempt.  

3.Question Generation 
   - LLM generates questions tailored to role & resume.  
   - Questions are sent one by one to the user.  

4.Answer Capture
   - User answers via audio.  
   - Audio → transcribed → analyzed (pacing, pauses, content relevance).  

5.Analysis & Feedback 
   - Workers process transcription & analysis jobs via SQS.  
   - Feedback stored as `QuestionAttempt` + aggregated.  

6.Final Report
   - Once interview ends → system generates a detailed performance report.  
   - Includes strengths, weaknesses, scores, and improvement tips.  

7.Drop-Off Handling
   - If user leaves midway, progress is saved in `InterviewAttempt`.  
   - They can resume later without losing data.  

3. Running Locally  

  1.Setup Environment  

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

  2.Configure Env Variables
  DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/samvaad
  OPENAI_API_KEY=...
  AWS_ACCESS_KEY_ID=...
  AWS_SECRET_ACCESS_KEY=...

  3.Start API Server
  uvicorn app.main:app --reload

  4.Explore APIs
  Swagger Docs → http://localhost:8000/docs

📌 Notes

This branch is part of the main Samvaad Saathi repo 
Main repo 🔗 https://github.com/Barabari-Project/Samvad-Sathi-AI. 


