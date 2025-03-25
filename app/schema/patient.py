from datetime import date

from pydantic import BaseModel, ConfigDict

from app.schema.enums import Sex


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
