from datetime import datetime, timezone

import pytest

from app.models import Job
from app.worker import generate_report


def make_job(attempts: int, fail_until: int = 0) -> Job:
    now = datetime.now(timezone.utc)
    return Job(id="job_abc", type="generate_report",
               payload={"title": "Test", "fail_until_attempt": fail_until}, status="processing",
               attempts=attempts, available_at=now, locked_at=now, worker_id="worker-a",
               created_at=now)


def test_report_generation_is_deterministic() -> None:
    assert generate_report(make_job(1), 0) == {"reportUrl": "/reports/report-abc.pdf"}


def test_deliberate_failure_supports_retry_experiment() -> None:
    with pytest.raises(RuntimeError, match="attempt 2"):
        generate_report(make_job(2, fail_until=2), 0)
