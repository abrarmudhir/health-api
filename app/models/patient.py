from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.enums import SexEnum


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex = Column(Enum(SexEnum), nullable=False)

    medication_requests = relationship("MedicationRequest", back_populates="patient")
