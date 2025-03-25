from pydantic import BaseModel, ConfigDict


class ClinicianBase(BaseModel):
    first_name: str
    last_name: str
    registration_id: str


class ClinicianCreate(ClinicianBase):
    pass


class ClinicianOut(ClinicianBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
