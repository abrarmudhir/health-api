from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.medication_request import MedicationRequestRepository
from app.schema.medication_request import MedicationRequestCreate, MedicationRequestOut

router = APIRouter(prefix="/medication_requests", tags=["Medication Requests"])


@router.post("/", response_model=MedicationRequestOut, status_code=201)
def create_medication_request(
    med_req_in: MedicationRequestCreate, db: Session = Depends(get_db)
):
    repo = MedicationRequestRepository(db)
    created_req = repo.create(med_req_in)
    return created_req
