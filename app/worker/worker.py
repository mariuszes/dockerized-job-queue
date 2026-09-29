import time
import random
import signal

from app.db.database import take_pending_job, finish_job, fail_job, requeue_job

MIN_CPU_ITERATIONS = 80_000_000
MAX_CPU_ITERATIONS = 120_000_000
MEMORY_MIB = 64

def run_workload() -> None:
    memory = bytearray(MEMORY_MIB * 1024 * 1024)

    result = 0

    cpu_iterations = random.randint(
        MIN_CPU_ITERATIONS,
        MAX_CPU_ITERATIONS,
    )

    for number in range(cpu_iterations):
        result += number * number

def handle_sigterm(_signum, _frame) -> None:
    print("Received SIGTERM. Requeuing job and exiting...")
    raise SystemExit


def process_job(job: dict) -> None:
    job_id = job["id"]
    payload = job["payload"]

    print(f"Starting job {job_id}")

    try:
        start = time.time()

        run_workload()

        elapsed = time.time() - start

        if payload == "fail": # only for testing
            raise RuntimeError("Fake worker error for testing")

        result = f"Processed: {payload} in {elapsed:.2f} seconds"

        finish_job(job_id, result)

        print(f"Finished job {job_id}")
    except SystemExit:
        requeue_job(job_id)
        print(f"Requeued job {job_id}")
        raise
    
    except Exception as error:
        error_message = f"Worker error: {error}"
        fail_job(job_id, error_message)

        print(f"Failed job {job_id}: {error}")


def main() -> None:
    signal.signal(signal.SIGTERM, handle_sigterm)

    print("Worker started")

    while True:
        job = take_pending_job()

        if job is None:
            print("No pending jobs found. Waiting...")
            time.sleep(5)
            continue

        process_job(job)


if __name__ == "__main__":
    main()