# users/services.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from users.models import User
from users.utils import hash_password, verify_google_token

def create_user(db: Session, user_data):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    hashed_pw = hash_password(user_data.password)

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_pw,
        degree=user_data.degree,
        university=user_data.university,
        date_of_birth=user_data.date_of_birth
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def signup_with_google(db: Session, google_token: str):
    idinfo = verify_google_token(google_token)
    if not idinfo:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = idinfo.get("email")
    name = idinfo.get("name", "Google User")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, password=None)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
