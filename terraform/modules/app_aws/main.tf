resource "aws_ecr_repository" "app" {
  name = "job-queue"
}

resource "aws_secretsmanager_secret" "app" {
  name = "job-queue/postgres-secrets"
}

data "aws_iam_policy_document" "pod_identity_assume_role" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole",
      "sts:TagSession"
    ]

    principals {
      type        = "Service"
      identifiers = ["pods.eks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "secret_access" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue"
    ]

    resources = [
      aws_secretsmanager_secret.app.arn
    ]
  }
}

resource "aws_iam_role" "api" {
  name = "job-queue-api-role"

  assume_role_policy = data.aws_iam_policy_document.pod_identity_assume_role.json
}

resource "aws_iam_role" "worker" {
  name = "job-queue-worker-role"

  assume_role_policy = data.aws_iam_policy_document.pod_identity_assume_role.json
}

resource "aws_iam_policy" "secret_access" {
  name   = "job-queue-secret-access"
  policy = data.aws_iam_policy_document.secret_access.json
}

resource "aws_iam_role_policy_attachment" "api_secret_access" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.secret_access.arn
}

resource "aws_iam_role_policy_attachment" "worker_secret_access" {
  role       = aws_iam_role.worker.name
  policy_arn = aws_iam_policy.secret_access.arn
}

resource "aws_eks_pod_identity_association" "api" {
  cluster_name    = var.cluster_name
  namespace       = "job-queue"
  service_account = "api-service-account"
  role_arn        = aws_iam_role.api.arn
}

resource "aws_eks_pod_identity_association" "worker" {
  cluster_name    = var.cluster_name
  namespace       = "job-queue"
  service_account = "worker-service-account"
  role_arn        = aws_iam_role.worker.arn
}
