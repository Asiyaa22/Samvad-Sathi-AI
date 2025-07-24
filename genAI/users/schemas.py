# users/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    degree: str
    university: str
    date_of_birth: str

class UserOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr

class GoogleToken(BaseModel):
    token: str
