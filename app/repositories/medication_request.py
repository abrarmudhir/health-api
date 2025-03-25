from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.medication_request import MedicationRequest
from app.schema.medication_request import (
    MedicationRequestCreate,
    MedicationRequestUpdate,
)


class MedicationRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, med_req_in: MedicationRequestCreate) -> MedicationRequest:
        med_req = MedicationRequest(**med_req_in.model_dump())
        self.db.add(med_req)
        self.db.commit()
        self.db.refresh(med_req)
        return med_req

    def get_all(
        self,
        status: Optional[str] = None,
        prescribed_from: Optional[datetime] = None,
        prescribed_to: Optional[datetime] = None,
    ) -> List[MedicationRequest]:
        query = self.db.query(MedicationRequest)
        if status:
            query = query.filter(MedicationRequest.status == status)
        if prescribed_from:
            query = query.filter(MedicationRequest.prescribed_date >= prescribed_from)
        if prescribed_to:
            query = query.filter(MedicationRequest.prescribed_date <= prescribed_to)
        return query.all()

    def update(
        self, med_req_id: int, med_req_update: MedicationRequestUpdate
    ) -> Optional[MedicationRequest]:
        med_req = (
            self.db.query(MedicationRequest)
            .filter(MedicationRequest.id == med_req_id)
            .first()
        )
        if not med_req:
            return None
        update_data = med_req_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(med_req, field, value)
        self.db.commit()
        self.db.refresh(med_req)
        return med_req
