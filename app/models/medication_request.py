from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums import RequestStatusEnum


class MedicationRequest(Base):
    __tablename__ = "medication_requests"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("clinicians.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    reason_text = Column(Text)
    prescribed_date = Column(DateTime, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    frequency = Column(String)
    status = Column(Enum(RequestStatusEnum), nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="medication_requests")
    clinician = relationship("Clinician", back_populates="medication_requests")
    medication = relationship("Medication", back_populates="medication_requests")
