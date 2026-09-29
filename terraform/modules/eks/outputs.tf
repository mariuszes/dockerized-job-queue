output "cluster_name" {
  value = aws_eks_cluster.job_queue.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.job_queue.endpoint
}
