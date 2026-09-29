import httpx


API_URL = "http://localhost:30081/jobs"
JOB_COUNT = 30


for number in range(1, JOB_COUNT + 1):
    response = httpx.post(
        API_URL,
        json={"payload": f"load-test-{number}"},
    )

    response.raise_for_status()

    job = response.json()

    print(f"Created job {job['id']}")


print(f"Created {JOB_COUNT} jobs")