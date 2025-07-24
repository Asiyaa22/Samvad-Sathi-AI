# interviews/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    job_role = Column(String(100))
    experience_years = Column(Integer)
    resume = Column(String(255))  # URL or file path
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", back_populates="interview")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_text = Column(Text)

    interview = relationship("Interview", back_populates="questions")


class InterviewAttempt(Base):
    __tablename__ = "interview_attempts"

    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    attempted_questions = Column(Integer, default=0)
    status = Column(String(50), default="in_progress")  # or completed, dropped
    started_at = Column(DateTime(timezone=True), server_default=func.now())


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True)
    interview_attempt_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    audio_url = Column(String(255))
    is_answered = Column(Boolean, default=False)
    is_transcribed = Column(Boolean, default=False)
    is_analysed = Column(Boolean, default=False)
    transcription = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
