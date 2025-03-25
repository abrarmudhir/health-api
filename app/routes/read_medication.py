from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.medication_request import MedicationRequestRepository
from app.schema.medication_request import MedicationRequestOut

router = APIRouter(prefix="/medication_requests", tags=["Medication Requests"])


@router.get("/", response_model=List[MedicationRequestOut])
def read_medication_requests(
    status: Optional[str] = Query(None, description="Filter by status"),
    prescribed_from: Optional[datetime] = Query(
        None, description="Filter for prescribed_date from (ISO format)"
    ),
    prescribed_to: Optional[datetime] = Query(
        None, description="Filter for prescribed_date to (ISO format)"
    ),
    db: Session = Depends(get_db),
):
    repo = MedicationRequestRepository(db)
    med_requests = repo.get_all(
        status=status, prescribed_from=prescribed_from, prescribed_to=prescribed_to
    )
    return med_requests
