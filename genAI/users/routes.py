# users/routes.py
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from users.schemas import UserSignup, UserOut, GoogleToken
from users.services import create_user, signup_with_google
from database import get_db_session

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(user: UserSignup, db: Session = Depends(get_db_session)):
    created_user = create_user(db, user)
    return {
        "user_id": created_user.id,
        "name": created_user.name,
        "email": created_user.email
    }

@router.post("/signup-google", response_model=UserOut)
def signup_google(payload: GoogleToken, db: Session = Depends(get_db_session)):
    user = signup_with_google(db, payload.token)
    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }
