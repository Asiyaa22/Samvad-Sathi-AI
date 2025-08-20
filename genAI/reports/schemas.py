from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ReportBase(BaseModel):
    interview_attempt_id: UUID
    summary: Optional[str] = None
    details: Optional[str] = None  # Can be JSON string

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    report_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
