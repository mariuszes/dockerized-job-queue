# Dockerized Job Queue Platform

The project started as a local Docker-based job queue built with Python, FastAPI, PostgreSQL, Docker Compose and nginx. Most sections below describe this original Docker version and its application flow.

The project was later extended with local Kubernetes on kind, Amazon EKS, Terraform-managed AWS infrastructure and GitHub Actions CD. These later stages are summarized near the end of this README and documented in more detail in `k8s/kind/`, `k8s/eks/`, `terraform/` and `history/hpa-cpu/`.

The application is a simple job queue platform. Users can create jobs through the API, check their status and read the final result. Each job is stored in PostgreSQL and processed by a separate worker container, which changes the job status from `pending` to `processing`, and then to `done` or `failed`.

The worker performs a synthetic CPU and memory workload for every job. It allocates 64 MiB of memory and runs between 80 and 120 million CPU operations, creating controlled variation in processing time. This makes it possible to observe resource usage, parallel processing across worker replicas and autoscaling behavior in Kubernetes.

## Features

* FastAPI backend with a separate worker container for background job processing
* PostgreSQL database with a Docker volume for data persistence
* nginx reverse proxy used as the only public entrypoint
* Dockerfile with multi-stage build and non-root application user
* Docker Compose setup with API, worker, PostgreSQL, nginx, public/private networks and healthchecks
* Environment and repository setup using `.env`, `.env.example`, `.dockerignore` and `.gitignore`
* Dev and prod Compose files, plus Makefile and PowerShell scripts for common commands
* Pytest integration tests for the main API flow
* GitHub Actions CI with Docker build, tests, Trivy image scan and GHCR image publishing

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

## CI

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

_GET /health_ - checks if the API is running.

`http://localhost:8080/health`

* **Readiness check**

_GET /ready_ - checks if the API can connect to PostgreSQL

`http://localhost:8080/ready`

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

## Kubernetes

While revisiting this project to learn Kubernetes, I practiced:

- Dynamic volume provisioning with StorageClass instead of manually creating PersistentVolumes
- Horizontal pod autoscaling and queue-based autoscaling with KEDA
- GatewayClass, Gateway and HTTPRoute objects for exposing the application
- Envoy Gateway as the controller and Envoy Proxy as the traffic entry point
- ServiceAccounts, RBAC and least-privilege access inside the cluster
- NetworkPolicy for restricting communication between workloads
- Kubernetes Secrets together with AWS Secrets Manager and the Secrets Store CSI Driver
- EKS Pod Identity for giving individual workloads access to AWS resources
- Running the same Kubernetes application locally with kind and remotely on Amazon EKS

The Kubernetes fundamentals from my previous Air Stations project, such as Deployments, ReplicaSets, Services, ConfigMaps, probes and StatefulSets, were reused here as known building blocks rather than learned again from scratch.

While working on the Kubernetes part of the project, I also read selected chapters from *Kubernetes Patterns* by Bilgin Ibryam and Roland Huß, mainly while building the local kind version and improving the Kubernetes manifests.

## AWS, Terraform and CD

While extending the project to AWS and automating its deployment, I practiced:

- Infrastructure as Code with Terraform modules
- Custom VPC, public subnets, routing and Internet Gateway
- Amazon EKS and managed worker node groups
- Amazon ECR for application images
- Amazon EBS CSI Driver and EKS Pod Identity Agent
- AWS Secrets Manager for application credentials
- Separate IAM roles for API, worker and cluster components
- GitHub Actions authentication to AWS through OIDC
- EKS Access Entries for GitHub Actions cluster access
- Remote Terraform state in an S3 bucket
- S3 state locking with `use_lockfile`
- Helm-based cluster bootstrap for shared Kubernetes components
- GitHub Actions CD from successful CI to ECR and EKS
- Automatic application rollout after publishing a new image

I initially created and explored the AWS infrastructure manually through the AWS Console to better understand the services I was using. After reading selected chapters from *Terraform: Up & Running* by Yevgeniy Brikman, I moved to implementing the IaC with Terraform, using the AWS and Terraform documentation alongside the book.

## Notes
A job with payload `fail` is used to simulate a worker error and test the `failed` status.


