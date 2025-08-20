from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from database import Base  # Assuming your base model is defined here

class Report(Base):
    __tablename__ = "reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to InterviewAttempt
    interview_attempt_id = Column(UUID(as_uuid=True), ForeignKey("interview_attempts.id", ondelete="CASCADE"), nullable=False)
    
    # Short overall summary (e.g. "Good communication, weak DSA skills")
    summary = Column(Text, nullable=True)
    
    # Detailed feedback, possibly a JSON blob (stored as string for now)
    details = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional relationship if you want to access attempt from report
    interview_attempt = relationship("InterviewAttempt", back_populates="report", lazy="joined")
