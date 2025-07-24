# interviews/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db_session
from interviews.schemas import *
from interviews.services import *

router = APIRouter()

@router.post("/interview/start", response_model=InterviewOut)
def start(payload: InterviewCreate, db: Session = Depends(get_db_session)):
    interview = start_interview(db, payload)
    return {"interview_id": interview.id, "message": "Interview created and questions generated"}

@router.post("/interview/{interview_id}/attempt")
def start_attempt(interview_id: int, user_id: int, db: Session = Depends(get_db_session)):
    attempt = create_interview_attempt(db, interview_id, user_id)
    return {"attempt_id": attempt.id}

@router.get("/interview/attempt/{attempt_id}/next", response_model=QuestionOut)
def get_question(attempt_id: int, db: Session = Depends(get_db_session)):
    q = get_next_question(db, attempt_id)
    return {"question_id": q.id, "question_text": q.question_text}

@router.post("/question/answer")
def submit(payload: AnswerSubmission, db: Session = Depends(get_db_session)):
    return submit_answer(db, payload)
