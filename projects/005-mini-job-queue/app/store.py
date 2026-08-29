import json
import random
import uuid
from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg.rows import dict_row

from app.models import Job


class PostgresJobStore:
    def __init__(self, database_url: str, *, max_attempts: int = 4) -> None:
        self.database_url = database_url
        self.max_attempts = max_attempts

    @contextmanager
    def _connection(self) -> Iterator[psycopg.Connection]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            yield connection

    def initialize(self) -> None:
        with open("app/schema.sql", encoding="utf-8") as schema:
            with self._connection() as connection:
                connection.execute(schema.read())

    def create(self, job_type: str, payload: dict) -> Job:
        job_id = f"job_{uuid.uuid4().hex}"
        with self._connection() as connection:
            row = connection.execute(
                """INSERT INTO jobs (id, type, payload, status)
                   VALUES (%s, %s, %s, 'queued') RETURNING *""",
                (job_id, job_type, json.dumps(payload)),
            ).fetchone()
        return Job.model_validate(row)

    def get(self, job_id: str) -> Job | None:
        with self._connection() as connection:
            row = connection.execute("SELECT * FROM jobs WHERE id = %s", (job_id,)).fetchone()
        return Job.model_validate(row) if row else None

    def claim(self, worker_id: str, lease_seconds: int) -> Job | None:
        # Row selection and ownership update share one transaction. SKIP LOCKED lets
        # another worker select a different row instead of waiting on this one.
        with self._connection() as connection:
            # A crash on the final permitted attempt must not leave a processing
            # row stranded forever. Lease expiry is the durable failure signal.
            connection.execute(
                """UPDATE jobs
                   SET status = 'failed', error = 'lease expired after final attempt',
                       locked_at = NULL, worker_id = NULL
                   WHERE status = 'processing' AND attempts >= %s
                     AND locked_at < now() - (%s * interval '1 second')""",
                (self.max_attempts, lease_seconds),
            )
            row = connection.execute(
                """
                WITH candidate AS (
                    SELECT id FROM jobs
                    WHERE attempts < %s AND available_at <= now()
                      AND (status = 'queued' OR
                           (status = 'processing' AND locked_at < now() - (%s * interval '1 second')))
                    ORDER BY available_at, created_at
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                )
                UPDATE jobs AS job
                SET status = 'processing', attempts = attempts + 1,
                    locked_at = now(), worker_id = %s, error = NULL
                FROM candidate
                WHERE job.id = candidate.id
                RETURNING job.*
                """,
                (self.max_attempts, lease_seconds, worker_id),
            ).fetchone()
        return Job.model_validate(row) if row else None

    def complete(self, job_id: str, worker_id: str, result: dict) -> bool:
        with self._connection() as connection:
            row = connection.execute(
                """UPDATE jobs SET status = 'completed', result = %s,
                       completed_at = now(), locked_at = NULL, worker_id = NULL
                   WHERE id = %s AND status = 'processing' AND worker_id = %s
                   RETURNING id""",
                (json.dumps(result), job_id, worker_id),
            ).fetchone()
        return row is not None

    def fail(self, job: Job, worker_id: str, error: str) -> bool:
        terminal = job.attempts >= self.max_attempts
        # Full jitter spreads simultaneous retries over [0, exponential cap].
        delay_seconds = random.uniform(0, 5 * (2 ** (job.attempts - 1)))
        with self._connection() as connection:
            row = connection.execute(
                """UPDATE jobs
                   SET status = %s, error = %s, locked_at = NULL, worker_id = NULL,
                       available_at = CASE WHEN %s THEN available_at
                                           ELSE now() + (%s * interval '1 second') END
                   WHERE id = %s AND status = 'processing' AND worker_id = %s
                   RETURNING id""",
                ("failed" if terminal else "queued", error[:1000], terminal,
                 delay_seconds, job.id, worker_id),
            ).fetchone()
        return row is not None
