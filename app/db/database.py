import psycopg

from app.core.config import DATABASE_URL

def check_database_connection() -> bool:
    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
        
        return result == (1,)

    except Exception as error:
        print(f"Databse connection error: {error}")
        return False
    

def create_job(payload: str) -> dict:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO jobs (status, payload)
                VALUES (%s, %s)
                RETURNING id, status, payload, result;
                """,
                ("pending", payload),
            )

            row = cursor.fetchone()

        connection.commit()
    
    return {
        "id": row[0],
        "status": row[1],
        "payload": row[2],
        "result": row[3],
    }


def get_jobs() -> list[dict]:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, status, payload, result
                FROM jobs
                ORDER BY id;
                """
            )

            rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append(
            {
                "id": row[0],
                "status": row[1],
                "payload": row[2],
                "result": row[3],
            }
        )

    return jobs


def get_job_by_id(job_id: int) -> dict | None:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, status, payload, result
                FROM jobs
                WHERE id = %s;
                """,
                (job_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "status": row[1],
        "payload": row[2],
        "result": row[3],
    }


def take_pending_job() -> dict | None:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE jobs
                SET status = 'processing',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = (
                    SELECT id
                    FROM jobs
                    WHERE status = 'pending'
                    ORDER BY id
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                )
                RETURNING id, status, payload, result;
                """
            )

            row = cursor.fetchone()

        connection.commit()

    if row is None:
        return None

    return {
        "id": row[0],
        "status": row[1],
        "payload": row[2],
        "result": row[3],
    }


def finish_job(job_id: int, result: str) -> None:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE jobs
                SET status = %s,
                    result = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                ("done", result, job_id),
            )

        connection.commit()


def fail_job(job_id: int, error_message: str) -> None:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE jobs
                SET status = %s,
                    result = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                ("failed", error_message, job_id),
            )

        connection.commit()
         