from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from reports import schemas, models
from database import get_db  # Your DB session dependency

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/{interview_attempt_id}", response_model=schemas.ReportResponse)
def get_report_by_attempt_id(
    interview_attempt_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Fetch the generated report for a specific interview attempt.
    """

    report = (
        db.query(models.Report)
        .filter(models.Report.interview_attempt_id == interview_attempt_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found for this attempt."
        )

    return report


# Optional route to list all reports (useful for admin or debugging)
@router.get("/", response_model=list[schemas.ReportResponse])
def list_all_reports(db: Session = Depends(get_db)):
    """
    List all reports (useful for debugging or admin access).
    """
    return db.query(models.Report).all()
