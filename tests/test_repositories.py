import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import RequestStatusEnum
from app.repositories.medication_request import MedicationRequestRepository
from app.schema.medication_request import (
    MedicationRequestCreate,
    MedicationRequestUpdate,
)


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


class TestRepositories:
    def test_create_medication_request(self, db_session):
        repo = MedicationRequestRepository(db_session)
        now = datetime.datetime.now()
        med_req_in = MedicationRequestCreate(
            patient_id=1,
            clinician_id=1,
            medication_id=1,
            reason_text="Test reason",
            prescribed_date=now,
            start_date=now,
            frequency="3 times per day",
            status="active",
            end_date=now + datetime.timedelta(days=7),
        )
        med_req = repo.create(med_req_in)
        assert med_req.id is not None
        assert med_req.patient_id == 1
        assert med_req.status == RequestStatusEnum.active

    def test_get_all_medication_requests(self, db_session):
        repo = MedicationRequestRepository(db_session)
        now = datetime.datetime.now()

        med_req_in1 = MedicationRequestCreate(
            patient_id=1,
            clinician_id=1,
            medication_id=1,
            reason_text="Reason 1",
            prescribed_date=now,
            start_date=now,
            frequency="3 times per day",
            status="active",
            end_date=now + datetime.timedelta(days=7),
        )
        med_req_in2 = MedicationRequestCreate(
            patient_id=2,
            clinician_id=2,
            medication_id=2,
            reason_text="Reason 2",
            prescribed_date=now + datetime.timedelta(days=1),
            start_date=now + datetime.timedelta(days=1),
            frequency="2 times per day",
            status="completed",
            end_date=now + datetime.timedelta(days=8),
        )
        repo.create(med_req_in1)
        repo.create(med_req_in2)

        active_requests = repo.get_all(status="active")
        assert len(active_requests) == 1
        all_requests = repo.get_all(
            prescribed_from=now - datetime.timedelta(days=1),
            prescribed_to=now + datetime.timedelta(days=2),
        )
        assert len(all_requests) == 2

    def test_update_medication_request(self, db_session):
        repo = MedicationRequestRepository(db_session)
        now = datetime.datetime.now()
        med_req_in = MedicationRequestCreate(
            patient_id=1,
            clinician_id=1,
            medication_id=1,
            reason_text="Update test",
            prescribed_date=now,
            start_date=now,
            frequency="3 times per day",
            status="active",
            end_date=now + datetime.timedelta(days=7),
        )
        med_req = repo.create(med_req_in)
        update_data = MedicationRequestUpdate(
            frequency="2 times per day",
            status="completed",
        )
        updated_med_req = repo.update(med_req.id, update_data)
        assert updated_med_req is not None
        assert updated_med_req.frequency == "2 times per day"
        assert updated_med_req.status == RequestStatusEnum.completed
