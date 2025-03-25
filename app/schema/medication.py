from pydantic import BaseModel, ConfigDict

from app.schema.enums import MedicationForm


class MedicationBase(BaseModel):
    code: str
    code_name: str
    code_system: str
    strength_value: float
    strength_unit: str
    form: MedicationForm


class MedicationCreate(MedicationBase):
    pass


class MedicationOut(MedicationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
