import time

from app.db.database import take_pending_job, finish_job, fail_job
from app.db.init_db import create_tables


def process_job(job: dict) -> None:
    job_id = job["id"]
    payload = job["payload"]

    print(f"Starting job {job_id}")

    try:
        time.sleep(60)

        if payload == "fail": # only for testing
            raise RuntimeError("Fake worker error for testing")

        result = f"Processed: {payload}"

        finish_job(job_id, result)

        print(f"Finished job {job_id}")

    except Exception as error:
        error_message = f"Worker error: {error}"
        fail_job(job_id, error_message)

        print(f"Failed job {job_id}: {error}")


def main() -> None:
    print("Worker started")

    create_tables()

    while True:
        job = take_pending_job()

        if job is None:
            print("No pending jobs found. Waiting...")
            time.sleep(5)
            continue

        process_job(job)


if __name__ == "__main__":
    main()