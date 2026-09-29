from fastapi import FastAPI, HTTPException

from app.db.database import check_database_connection, create_job, get_jobs, get_job_by_id
from app.schemas.job import JobCreate

app = FastAPI(
    title="Dockerized Job Queue Platform",
)

@app.get("/health")
def health():
    return {
        "status": "ok",
    }

@app.get("/ready")
def ready():
    database_ok = check_database_connection()

    if database_ok:
        return {
            "status": "ok",
            "database": "connected",
        }

    raise HTTPException(
        status_code=503,
        detail="Database not connected",
    )

@app.post("/jobs")
def add_job(job: JobCreate):
    new_job = create_job(job.payload)
    return new_job

@app.get("/jobs")
def list_jobs():
    return get_jobs()

@app.get("/jobs/{job_id}")
def get_single_job(job_id: int):
    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job