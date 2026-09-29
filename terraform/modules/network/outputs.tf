output "vpc_id" {
  value = aws_vpc.job_queue.id
}

output "public_subnet_ids" {
  value = values(aws_subnet.public)[*].id
}
