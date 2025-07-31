# 🧠 Samvaad Saathi — AI-Powered Interview Simulator

Samvaad Saathi is an AI-powered ed-tech platform designed to simulate real interview environments. It enables students to practice interviews, receive automated questions, submit responses (voice/text), and get intelligent feedback powered by LLMs.

> ⚠️ This is a **development branch** maintained by **Asiya Hashmi**, built on top of the **main repository** maintained by **Smit**.  
> The overall architecture and core features remain the same, but this branch focuses on modularizing and scaling backend functionalities.

---

## 🚀 Tech Stack

- **Backend**: FastAPI
- **LLM Integration**: OpenAI / Custom prompts
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Queueing**: AWS SQS (for async tasks like audio transcription & analysis)
- **Deployment**: AWS EC2 (Monolith Decoupled Architecture)
- **Others**: Pytest for testing (in progress)

---

## 📁 Folder Structure Overview
```
Samvaad-Saathi-AI/
│
├── genAI/
│ ├── interviews/
│ │ ├── models.py # SQLAlchemy models for Interview, Question, Attempts
│ │ ├── schemas.py # Pydantic schemas for request/response validation
│ │ ├── services.py # Core business logic for interview workflows
│ │ ├── routes.py # FastAPI routes for interview-related APIs
│ │
│ ├── users/ # (Completed) User registration and authentication
│ ├── sessions/ # (Completed) Session creation and login logic
│ │
│ ├── core/
│ │ ├── llm.py # Functions for LLM calls (e.g., question generation, analysis)
│ │ ├── sqs.py # SQS queue helpers for sending/receiving messages
│ │ └── prompts.py # Centralized LLM prompt templates for interviews & analysis
│ │
│ ├── workers/
│ │ └── analysis_worker.py # Worker to process SQS messages: transcribe + analyze answers
│
├── tests/ # (To be added) Unit and integration tests
│
├── main.py # FastAPI app entry point
├── requirements.txt # Project dependencies
└── README.md # Project documentation (this file)

```
---

## 🧩 Modules Explained

### 🔹 `interviews/`
Handles the full interview lifecycle:
- Start new interview sessions
- Fetch next questions
- Submit and track answers
- Mark interview as complete

**Files:**
- `models.py`: Database tables — Interview, Question, Attempts
- `schemas.py`: Input/output models using Pydantic
- `services.py`: Functions for each interview action (start, next Q, submit)
- `routes.py`: API endpoints for frontend/backend integration

---

### 🔹 `core/`
Utility and shared logic modules:
- `llm.py`: Calls OpenAI for generating questions and evaluating answers
- `prompts.py`: Houses reusable LLM prompt templates
- `sqs.py`: Manages AWS SQS queues for async processing (like transcription/analysis)

---

### 🔹 `workers/`
Background workers to handle time-consuming tasks:
- `analysis_worker.py`: 
  - Pulls messages from SQS
  - Transcribes audio answers
  - Analyzes response via LLM
  - Persists feedback in DB

---

### 🔹 `users/` & `sessions/`
Authentication and user/session management:
- User registration & login
- Session tracking

---

## 🏗️ Architecture

This project follows a **Decoupled Monolith Architecture**:
- Modular services (but deployed together)
- Clear separation of concerns
- Easy to scale/refactor into microservices later

Async-heavy tasks (e.g., audio analysis) are **decoupled via queues** and background workers to keep the app fast and responsive.

---

## 🧪 Branch Info

This branch is being developed by **Asiya Farhath** under Barabari’s development team.  
Key objectives of this branch:
- Refactor legacy monolith (`server.py`) into clean modules
- Improve testability and scalability
- Own and implement LLM features with better abstraction
- Implement backend services

🔄 You can find the **main repo and production branch** managed by **Smit** 🔗 https://github.com/Barabari-Project/Samvad-Sathi-AI.



## 👩‍💻 Contributor

**Asiya Farhath** — Digital Excellence Manager at Barabari  
Maintaining clean, production-grade backend with AI integrations.

