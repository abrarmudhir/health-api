from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from app.schema.clinician import ClinicianCreate
from app.schema.enums import Sex, MedicationForm, RequestStatus
from app.schema.medication import MedicationCreate
from app.schema.medication_request import (
    MedicationRequestCreate,
    MedicationRequestUpdate,
)
from app.schema.patient import PatientCreate


class TestSchemas:
    def test_patient_create_valid(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "sex": "male",
        }
        patient = PatientCreate(**data)
        assert patient.first_name == "John"
        assert patient.sex == Sex.male

    def test_patient_create_invalid_sex(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "sex": "unknown",
        }
        with pytest.raises(ValidationError):
            PatientCreate(**data)

    def test_clinician_create_valid(self):
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "registration_id": "REG123",
        }
        clinician = ClinicianCreate(**data)
        assert clinician.registration_id == "REG123"

    def test_medication_create_valid(self):
        data = {
            "code": "12345",
            "code_name": "TestMed",
            "code_system": "SNOMED",
            "strength_value": 5.0,
            "strength_unit": "mg",
            "form": "tablet",
        }
        medication = MedicationCreate(**data)
        assert medication.form == MedicationForm.tablet

    def test_medication_request_create_valid(self):
        now = datetime.now()
        data = {
            "patient_id": 1,
            "clinician_id": 2,
            "medication_id": 3,
            "reason_text": "Pain relief",
            "prescribed_date": now.isoformat(),
            "start_date": now.isoformat(),
            "frequency": "3 times per day",
            "status": "active",
            "end_date": (now + timedelta(days=7)).isoformat(),
        }
        med_req = MedicationRequestCreate(**data)
        assert med_req.status == RequestStatus.active
        assert med_req.end_date is not None

    def test_medication_request_update_valid(self):
        data = {
            "frequency": "2 times per day",
            "status": "completed",  # valid enum
        }
        med_req_update = MedicationRequestUpdate(**data)
        assert med_req_update.frequency == "2 times per day"
        assert med_req_update.status == RequestStatus.completed

    def test_medication_request_update_invalid_status(self):
        data = {
            "frequency": "2 times per day",
            "status": "invalid_status",
        }
        with pytest.raises(ValidationError):
            MedicationRequestUpdate(**data)
