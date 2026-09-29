import os

import httpx


BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8080")


def test_health_endpoint():
    response = httpx.get(f"{BASE_URL}/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

def test_ready_endpoint():
    response = httpx.get(f"{BASE_URL}/ready")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["database"] == "connected"


def test_create_job():
    response = httpx.post(
        f"{BASE_URL}/jobs",
        json={
            "payload": "pytest test job"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["status"] == "pending"
    assert data["payload"] == "pytest test job"
    assert data["result"] is None


def test_list_jobs():
    response = httpx.get(f"{BASE_URL}/jobs")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_single_job():
    create_response = httpx.post(
        f"{BASE_URL}/jobs",
        json={
            "payload": "single job test"
        },
    )

    created_job = create_response.json()
    job_id = created_job["id"]

    get_response = httpx.get(f"{BASE_URL}/jobs/{job_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == job_id
    assert data["payload"] == "single job test"


def test_get_missing_job_returns_404():
    response = httpx.get(f"{BASE_URL}/jobs/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Job not found"