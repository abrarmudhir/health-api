from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.medication_request import MedicationRequestRepository
from app.schema.medication_request import MedicationRequestOut, MedicationRequestUpdate

router = APIRouter(prefix="/medication_requests", tags=["Medication Requests"])


@router.patch("/{med_req_id}", response_model=MedicationRequestOut)
def update_medication_request(
    med_req_id: int,
    med_req_update: MedicationRequestUpdate,
    db: Session = Depends(get_db),
):
    repo = MedicationRequestRepository(db)
    updated_req = repo.update(med_req_id, med_req_update)
    if not updated_req:
        raise HTTPException(status_code=404, detail="Medication request not found")
    return updated_req
