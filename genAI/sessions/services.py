# sessions/services.py
from users.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from sessions.models import UserSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_session(db: Session, email: str, password: str) -> UserSession:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Check if already has active session
    #not needed 
    existing = db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.active_session == True
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Active session already exists.")

    session = UserSession(user_id=user.id, active_session=True)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def end_session(db: Session, user_id: int) -> UserSession:
    # Find the active session for the user
    session = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.active_session == True
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="No active session found.")

    # Update logout time and mark session as inactive
    session.logout_time = datetime.now()
    session.active_session = False
    db.commit()
    return session
