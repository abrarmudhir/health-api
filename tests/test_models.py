import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.models.clinician import Clinician
from app.models.enums import SexEnum, MedicationFormEnum, RequestStatusEnum
from app.models.medication import Medication
from app.models.medication_request import MedicationRequest
from app.models.patient import Patient


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


class TestModels:
    def test_create_patient(self, db_session):
        """Test creation and retrieval of a Patient."""
        patient = Patient(
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            sex=SexEnum.male,
        )
        db_session.add(patient)
        db_session.commit()
        db_session.refresh(patient)

        retrieved = db_session.get(Patient, patient.id)
        assert retrieved is not None
        assert retrieved.first_name == "John"
        assert retrieved.sex == SexEnum.male

    def test_create_clinician(self, db_session):
        """Test creation and retrieval of a Clinician."""
        clinician = Clinician(
            first_name="Alice",
            last_name="Smith",
            registration_id="REG123",
        )
        db_session.add(clinician)
        db_session.commit()
        db_session.refresh(clinician)

        retrieved = db_session.get(Clinician, clinician.id)
        assert retrieved is not None
        assert retrieved.registration_id == "REG123"

    def test_create_medication(self, db_session):
        """Test creation and retrieval of a Medication."""
        medication = Medication(
            code="747006",
            code_name="Oxamniquine",
            code_system="SNOMED",
            strength_value=5.0,
            strength_unit="g/ml",
            form=MedicationFormEnum.tablet,
        )
        db_session.add(medication)
        db_session.commit()
        db_session.refresh(medication)

        retrieved = db_session.get(Medication, medication.id)
        assert retrieved is not None
        assert retrieved.form == MedicationFormEnum.tablet

    def test_create_medication_request(self, db_session):
        """Test creation and retrieval of a MedicationRequest."""
        patient = Patient(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=datetime.date(1985, 5, 15),
            sex=SexEnum.female,
        )
        clinician = Clinician(
            first_name="Bob",
            last_name="Brown",
            registration_id="REG456",
        )
        medication = Medication(
            code="123456",
            code_name="Aspirin",
            code_system="SNOMED",
            strength_value=250.0,
            strength_unit="mg",
            form=MedicationFormEnum.capsule,
        )
        db_session.add_all([patient, clinician, medication])
        db_session.commit()
        db_session.refresh(patient)
        db_session.refresh(clinician)
        db_session.refresh(medication)

        now = datetime.datetime.now()
        med_request = MedicationRequest(
            patient_id=patient.id,
            clinician_id=clinician.id,
            medication_id=medication.id,
            reason_text="Pain relief",
            prescribed_date=now,
            start_date=now,
            end_date=now + datetime.timedelta(days=7),
            frequency="3 times / day",
            status=RequestStatusEnum.active,
        )
        db_session.add(med_request)
        db_session.commit()
        db_session.refresh(med_request)

        retrieved = db_session.get(MedicationRequest, med_request.id)
        assert retrieved is not None
        assert retrieved.status == RequestStatusEnum.active
        assert retrieved.frequency == "3 times / day"
