# interviews/schemas.py

from pydantic import BaseModel
from typing import Optional, List

class InterviewCreate(BaseModel):
    user_id: int
    session_id: int
    job_role: str
    experience_years: int
    resume_url: str  # Assuming already uploaded to S3

class InterviewOut(BaseModel):
    interview_id: int
    message: str

class QuestionOut(BaseModel):
    question_id: int
    question_text: str

class AnswerSubmission(BaseModel):
    interview_attempt_id: int
    question_id: int
    audio_url: str
