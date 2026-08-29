from fastapi import Depends, FastAPI, HTTPException, status

from app.config import Settings
from app.models import CreatedJob, JobView, ReportRequest
from app.store import PostgresJobStore


def create_app(store: PostgresJobStore | None = None) -> FastAPI:
    app = FastAPI(title="Mini Job Queue")
    settings = Settings()
    app.state.store = store or PostgresJobStore(settings.database_url, max_attempts=settings.max_attempts)

    def get_store() -> PostgresJobStore:
        return app.state.store

    @app.on_event("startup")
    def initialize_schema() -> None:
        app.state.store.initialize()

    @app.post("/reports", response_model=CreatedJob, status_code=status.HTTP_202_ACCEPTED)
    def create_report(request: ReportRequest, jobs: PostgresJobStore = Depends(get_store)) -> CreatedJob:
        job = jobs.create("generate_report", request.model_dump())
        return CreatedJob(jobId=job.id)

    @app.get("/jobs/{job_id}", response_model=JobView)
    def get_job(job_id: str, jobs: PostgresJobStore = Depends(get_store)) -> JobView:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="job not found")
        return JobView(status=job.status, attempts=job.attempts, result=job.result, error=job.error)

    return app


app = create_app()
