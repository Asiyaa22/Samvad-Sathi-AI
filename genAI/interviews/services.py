# interviews/services.py

from sqlalchemy.orm import Session
from interviews.models import Interview, Question, InterviewAttempt, QuestionAttempt
from fastapi import HTTPException
from interviews.schemas import AnswerSubmission
from core.llm import process_resume_from_s3_and_generate_questions
from core.analysis_sqs import publish_to_analysis_queue  # Assume core utils

async def start_interview(db: Session, payload):
    # Create interview entry
    interview = Interview(
        user_id=payload.user_id,
        session_id=payload.session_id,
        job_role=payload.job_role,
        experience_years=payload.experience_years,
        resume=payload.resume_url
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)

    # Generate questions using LLM logic
    # questions = process_resume_from_s3_and_generate_questions(payload.resume_url, payload.job_role)
    questions = await process_resume_from_s3_and_generate_questions(
       s3_url=payload.resume_url,
       target_job=payload.job_role,
       number_of_ques=payload.number_of_questions,
       job_description=payload.job_description
   )

    
    for q in questions:
        db.add(Question(interview_id=interview.id, question_text=q))
    db.commit()

    return interview

def create_interview_attempt(db: Session, interview_id: int, user_id: int):
    attempt = InterviewAttempt(interview_id=interview_id, user_id=user_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

def get_next_question(db: Session, attempt_id: int):
    attempt = db.query(InterviewAttempt).filter_by(id=attempt_id).first()
    if not attempt:
        raise HTTPException(404, "Interview attempt not found")

    interview_id = attempt.interview_id

    # Get unattempted question
    subquery = db.query(QuestionAttempt.question_id).filter_by(interview_attempt_id=attempt_id)
    next_q = db.query(Question).filter(
        Question.interview_id == interview_id,
        ~Question.id.in_(subquery)
    ).first()

    if not next_q:
        raise HTTPException(404, "No more questions")

    return next_q

def submit_answer(db: Session, payload: AnswerSubmission):
    # Store the answer attempt
    attempt = QuestionAttempt(
        interview_attempt_id=payload.interview_attempt_id,
        question_id=payload.question_id,
        audio_url=payload.audio_url,
        is_answered=True
    )
    db.add(attempt)

    # Increment counter in InterviewAttempt
    parent = db.query(InterviewAttempt).filter_by(id=payload.interview_attempt_id).first()
    parent.attempted_questions += 1

    db.commit()

    # Publish to SQS
    publish_to_analysis_queue({
        "question_attempt_id": attempt.id,
        "interview_attempt_id": payload.interview_attempt_id,
        "question_id": payload.question_id,
        "audio_url": payload.audio_url
    })

    return {"message": "Answer received and queued for analysis"}
