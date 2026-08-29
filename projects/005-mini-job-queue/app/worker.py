import logging
import os
import socket
import time

from app.config import Settings
from app.models import Job
from app.store import PostgresJobStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def generate_report(job: Job, processing_seconds: float) -> dict[str, str]:
    time.sleep(processing_seconds)
    if job.attempts <= int(job.payload.get("fail_until_attempt", 0)):
        raise RuntimeError(f"deliberate failure on attempt {job.attempts}")
    report_id = job.id.removeprefix("job_")
    return {"reportUrl": f"/reports/report-{report_id}.pdf"}


def run() -> None:
    settings = Settings()
    worker_id = os.getenv("WORKER_ID", f"{socket.gethostname()}-{os.getpid()}")
    store = PostgresJobStore(settings.database_url, max_attempts=settings.max_attempts)
    store.initialize()
    logger.info("worker %s started", worker_id)
    while True:
        job = store.claim(worker_id, settings.lease_seconds)
        if job is None:
            time.sleep(settings.poll_interval_seconds)
            continue
        logger.info("%s -> processing attempt %d", job.id, job.attempts)
        try:
            result = generate_report(job, settings.processing_seconds)
        except Exception as exc:  # the worker boundary turns failures into durable state
            store.fail(job, worker_id, str(exc))
            logger.exception("%s failed", job.id)
        else:
            if store.complete(job.id, worker_id, result):
                logger.info("%s -> completed", job.id)
            else:
                logger.warning("%s lost its lease before completion", job.id)


if __name__ == "__main__":
    run()
