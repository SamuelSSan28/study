from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

JobStatus = Literal["queued", "processing", "completed", "failed"]


class ReportRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    fail_until_attempt: int = Field(default=0, ge=0, le=10)


class Job(BaseModel):
    id: str
    type: str
    payload: dict[str, Any]
    status: JobStatus
    attempts: int
    available_at: datetime
    locked_at: datetime | None = None
    worker_id: str | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime
    completed_at: datetime | None = None


class CreatedJob(BaseModel):
    jobId: str
    status: Literal["queued"] = "queued"


class JobView(BaseModel):
    status: JobStatus
    attempts: int
    result: dict[str, Any] | None = None
    error: str | None = None
