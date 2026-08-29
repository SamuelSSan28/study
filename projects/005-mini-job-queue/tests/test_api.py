from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.api import create_app
from app.models import Job


def job(job_id: str = "job_123", status: str = "queued") -> Job:
    now = datetime.now(timezone.utc)
    return Job(id=job_id, type="generate_report", payload={"title": "Sales"},
               status=status, attempts=0, available_at=now, created_at=now)


class FakeStore:
    def __init__(self) -> None:
        self.jobs: dict[str, Job] = {}

    def initialize(self) -> None:
        pass

    def create(self, job_type: str, payload: dict) -> Job:
        created = job()
        created.type = job_type
        created.payload = payload
        self.jobs[created.id] = created
        return created

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)


def test_create_report_returns_accepted_job() -> None:
    store = FakeStore()
    with TestClient(create_app(store)) as client:
        response = client.post("/reports", json={"title": "Quarterly sales"})

    assert response.status_code == 202
    assert response.json() == {"jobId": "job_123", "status": "queued"}
    assert store.jobs["job_123"].payload == {"title": "Quarterly sales", "fail_until_attempt": 0}


def test_get_job_exposes_lifecycle_without_payload() -> None:
    store = FakeStore()
    completed = job(status="completed")
    completed.attempts = 1
    completed.result = {"reportUrl": "/reports/report-123.pdf"}
    store.jobs[completed.id] = completed
    with TestClient(create_app(store)) as client:
        response = client.get("/jobs/job_123")

    assert response.status_code == 200
    assert response.json() == {"status": "completed", "attempts": 1,
                               "result": {"reportUrl": "/reports/report-123.pdf"}, "error": None}


def test_missing_job_is_not_found() -> None:
    with TestClient(create_app(FakeStore())) as client:
        assert client.get("/jobs/missing").status_code == 404
