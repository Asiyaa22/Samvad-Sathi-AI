# sessions/routes.py
from users.models import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sessions.services import create_session, end_session
from sessions.schemas import SessionCreate, SessionOut, SessionEndRequest, SessionEndResponse
from database import get_db_session

router = APIRouter()

# ✅ Create a new login session
# sirf session create karne ka endpoint
#noun best practise
@router.post("/login", response_model=SessionOut)
def login_session(payload: SessionCreate, db: Session = Depends(get_db_session)):
    session = create_session(db, email=payload.email, password=payload.password)

    return {
        "message": "Session created successfully",
        "session_id": session.id,
        "user_id": session.user_id,
        "login_time": session.login_time
    }

# ✅ End an active session
@router.post("/logout", response_model=SessionEndResponse)
def logout_session(payload: SessionEndRequest, db: Session = Depends(get_db_session)):
    """
    Ends the active session for the given user ID.
    """
    session = end_session(db, payload.user_id)
    return {
        "message": "Session ended",
        "session_id": session.id,
        "user_id": session.user_id,
        "logout_time": session.logout_time
    }
