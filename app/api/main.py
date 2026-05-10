from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.db.init_db import create_tables

from app.db.database import check_database_connection, create_job, get_jobs, get_job_by_id
from app.schemas.job import JobCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # code when turning on
    create_tables()
    yield # fastapi works
    # code when turning off

app = FastAPI(
    title="Dockerized Job Queue Platform",
    lifespan=lifespan
)

@app.get("/health")
def health():
    database_ok = check_database_connection()

    if database_ok:
        return {
            "status": "ok",
            "database": "connected",
        }

    return {
        "status": "error",
        "database": "not connected",
    }

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