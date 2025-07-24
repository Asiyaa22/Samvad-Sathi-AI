# sessions/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class SessionCreate(BaseModel):
    email: EmailStr
    password: str 

class SessionOut(BaseModel):
    session_id: int
    login_time: datetime

class SessionEndRequest(BaseModel):
    user_id: int

class SessionEndResponse(BaseModel):
    message: str
    session_id: int
    logout_time: str
