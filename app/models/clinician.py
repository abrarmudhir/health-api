from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Clinician(Base):
    __tablename__ = "clinicians"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    registration_id = Column(String, unique=True, nullable=False)

    medication_requests = relationship("MedicationRequest", back_populates="clinician")
