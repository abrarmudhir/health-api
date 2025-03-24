from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.enums import MedicationFormEnum


class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
    code_system = Column(String, nullable=False)
    strength_value = Column(Float, nullable=False)
    strength_unit = Column(String, nullable=False)
    form = Column(Enum(MedicationFormEnum), nullable=False)

    medication_requests = relationship("MedicationRequest", back_populates="medication")
