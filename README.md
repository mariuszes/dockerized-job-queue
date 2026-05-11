# Dockerized Job Queue Platform

A small DevOps-focused project using Python, FastAPI, PostgreSQL, Docker, Docker Compose and Nginx.

The application is a simple job queue platform. Users can create jobs through the API, check their status and read the final result. Each job is stored in PostgreSQL and processed by a separate worker container, which changes the job status from `pending` to `processing`, and then to `done` or `failed`.

The worker simulates a longer background task by waiting 60 seconds before finishing the job. This is meant to imitate real situations where some tasks take more time because of computation, memory usage or external processing. Thanks to this, the platform can later be extended for learning Kubernetes concepts such as scaling workers, handling multiple jobs, resource limits and basic optimization.

## Features

* FastAPI backend with a separate worker container for background job processing
* PostgreSQL database with a Docker volume for data persistence
* nginx reverse proxy used as the only public entrypoint
* Dockerfile with multi-stage build and non-root application user
* Docker Compose setup with API, worker, PostgreSQL, nginx, public/private networks and healthchecks
* Environment and repository setup using `.env`, `.env.example`, `.dockerignore` and `.gitignore`
* Dev and prod Compose files, plus Makefile and PowerShell scripts for common commands
* Pytest integration tests for the main API flow
* GitHub Actions CI/CD with Docker build, tests, Trivy image scan and GHCR image publishing

## Architecture

The application consists of four containers:

1. `nginx` - reverse proxy and public entrypoint

2. `api` - FastAPI application used to create and read jobs

3. `worker` - background process that handles pending jobs

4. `postgres` - database for jobs, statuses and results

**Request flow:**

`User` &rarr; `nginx` &rarr; `api` &rarr; `postgres`

**Worker flow:**

`worker` &rarr; `postgres`



## Docker Networks

The containers communicate through two Docker networks:

* `public_net` - used by `nginx` and `api`
* `private_net` - used by `api`, `worker` and `postgres`

Only nginx exposes a public port. PostgreSQL is not exposed outside Docker.

## How to Run

You can start the environment with the included `Makefile` commands on Linux/macOS or with PowerShell scripts from the `scripts/` folder on Windows.

Development mode starts the full stack with live reload enabled for the API.

## Dev and Prod Setup

**Development mode uses:**

* `docker-compose.yml`
* `docker-compose.dev.yml`
* FastAPI `--reload`
* local `app` folder mounted into the API and worker containers

Run development mode:

`./scripts/dev.ps1` or `make dev`

**Production-like mode uses:**

* `docker-compose.yml`
* `docker-compose.prod.yml`
* application code from the built Docker image
* no FastAPI reload
* no local source code volume mounted into containers

Run production mode:

`./scripts/prod.ps1` or `make prod`

## Tests

The integration test suite uses pytest and httpx to validate the main API flow:
* health endpoint
* creating a job
* listing jobs
* getting one job by ID
* 404 response for missing job

Run tests locally:

`pytest`
or
`./scripts/test.ps1`

## CI/CD

GitHub Actions runs the project workflow automatically after push or pull request.

The workflow includes:

1. building the Docker image

2. starting the Docker Compose stack

3. waiting for `/health` through nginx

4. running pytest integration tests

5. scanning the Docker image with Trivy

6. publishing the image to GitHub Container Registry

Trivy currently uses `exit-code 0`, because the scan may report HIGH vulnerabilities from system packages in the base Python/Debian image, not directly from the application code. The scan still reports findings in CI.

## Available Pages and API Routes

* **Swagger documentation**

_GET /docs_ - opens FastAPI Swagger UI.

`http://localhost:8080/docs`

* **Health check**

_GET /health_ - checks if the API and database connection are working.

`http://localhost:8080/health`

* **Create job**

_POST /jobs_ - creates a new job with `pending` status.

Example body:

```json
{
  "payload": "test job"
}
```

* **List jobs**

_GET /jobs_ - returns all jobs from the database.

`http://localhost:8080/jobs`

* **Get job by ID**

_GET /jobs/{job_id}_ - returns one selected job.

Example:

`http://localhost:8080/jobs/1`

## Notes
A job with payload `fail` is used to simulate a worker error and test the `failed` status.


