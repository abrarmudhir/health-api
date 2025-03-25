import datetime
from typing import Any, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.repositories.medication_request import MedicationRequestRepository
from app.routes.create_medication import router as med_req_router
from app.schema.medication_request import MedicationRequestCreate


def fake_create(
    self: MedicationRequestRepository, med_req_in: MedicationRequestCreate
) -> Dict[str, Any]:
    data = med_req_in.model_dump()
    data["id"] = 1
    return data


@pytest.fixture
def app_with_mock(monkeypatch) -> FastAPI:
    monkeypatch.setattr(MedicationRequestRepository, "create", fake_create)

    app = FastAPI()
    app.include_router(med_req_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


@pytest.fixture
def client(app_with_mock: FastAPI) -> TestClient:
    return TestClient(app_with_mock)


class TestAPI:
    def test_create_medication_request(self, client: TestClient) -> None:
        now = datetime.datetime.now()
        now_iso = now.isoformat()
        payload = {
            "patient_id": 1,
            "clinician_id": 1,
            "medication_id": 1,
            "reason_text": "Test reason",
            "prescribed_date": now_iso,
            "start_date": now_iso,
            "frequency": "3 times per day",
            "status": "active",
            "end_date": (now + datetime.timedelta(days=7)).isoformat(),
        }

        response = client.post("/medication_requests/", json=payload)
        assert response.status_code == 201, response.text

        data = response.json()
        assert data["id"] == 1
        assert data["patient_id"] == payload["patient_id"]
        assert data["status"] == "active"
