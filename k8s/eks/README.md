# Kubernetes EKS setup

Short description of the AWS/EKS variant of this project. The local Kubernetes setup remains in `k8s/kind`, while this directory contains the AWS-specific Kustomize overlay and patches.

## EKS overlay
##### AWS-specific Kubernetes configuration
`k8s/eks` reuses the resources from `k8s/kind` and changes only the parts required for AWS, such as the ECR image, EBS storage, AWS Secrets Manager integration and the external Envoy LoadBalancer.

This keeps the local kind environment independent from the EKS-specific configuration.

## Infrastructure
##### AWS resources are managed with Terraform
The EKS cluster and the AWS resources used by this deployment are provisioned from the `terraform` directory. A more detailed description of the infrastructure and its design decisions is kept in `terraform/README.md`.

## Cluster bootstrap
##### Install cluster-wide components
The Helm commands used to install or update the cluster-wide components are stored in:

```text
.github/workflows/cluster-bootstrap.yml
```

This manually triggered workflow installs the Secrets Store CSI Driver, AWS Secrets Manager provider, KEDA and Envoy Gateway. These Helm-managed components are kept in a separate bootstrap workflow instead of being mixed into the Terraform infrastructure.

## Continuous deployment
##### Deploy the application to EKS
The EKS deployment process is defined in `.github/workflows/cd.yml`, which runs after a successful CI workflow, pushes the application image to ECR and deploys the manifests to the cluster.

## Secrets
##### AWS Secrets Manager and Secrets Store CSI Driver
Credentials are stored in AWS Secrets Manager and retrieved through the Secrets Store CSI Driver with EKS Pod Identity. `syncSecret.enabled=true` also synchronizes them into the Kubernetes Secret `sms-postgres-credentials-secret`, so the same values are additionally stored in etcd.

A cleaner setup would consume CSI-mounted files directly, but that would require changing how the existing application and PostgreSQL receive their configuration. While working on the EKS deployment, I focused more on learning AWS infrastructure and Kubernetes-to-AWS integration than on rewriting the application itself.

## Design decisions and simplifications
##### Deliberate project trade-offs
- API and worker use CSI mounts and separate EKS Pod Identity roles, while PostgreSQL reuses the synchronized Kubernetes Secret instead of repeating the same Pod Identity and CSI setup.
- CD uses the `latest` ECR tag, so each deployment triggers `kubectl rollout restart` to make the Pods pull the updated image. A better approach would use commit-specific tags instead, so Kubernetes can detect the image change directly without forcing a restart every time.
