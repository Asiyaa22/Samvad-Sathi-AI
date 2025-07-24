from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)  # session_id
    user_id = Column(Integer, nullable=False)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    logout_time = Column(DateTime(timezone=True), nullable=True)
    active_session = Column(Boolean, default=True)
