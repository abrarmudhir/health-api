from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schema.enums import RequestStatus


class MedicationRequestBase(BaseModel):
    patient_id: int
    clinician_id: int
    medication_id: int
    reason_text: Optional[str] = None
    prescribed_date: datetime
    start_date: datetime
    frequency: str
    status: RequestStatus


class MedicationRequestCreate(MedicationRequestBase):
    end_date: Optional[datetime] = None


class MedicationRequestUpdate(BaseModel):
    end_date: Optional[datetime] = None
    frequency: Optional[str] = None
    status: Optional[RequestStatus] = None


class MedicationRequestOut(MedicationRequestBase):
    id: int
    end_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
