resource "aws_vpc" "job_queue" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "job-queue-vpc"
  }
}

resource "aws_subnet" "public" {
  for_each = var.public_subnets

  vpc_id                  = aws_vpc.job_queue.id
  cidr_block              = each.value.cidr
  availability_zone       = each.value.az
  map_public_ip_on_launch = true

  tags = {
    Name                     = "job-queue-${each.key}"
    "kubernetes.io/role/elb" = "1"
  }
}

resource "aws_internet_gateway" "job_queue" {
  vpc_id = aws_vpc.job_queue.id

  tags = {
    Name = "job-queue-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.job_queue.id

  tags = {
    Name = "job-queue-public-rt"
  }
}

resource "aws_route" "internet" {
  route_table_id = aws_route_table.public.id

  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.job_queue.id
}

resource "aws_route_table_association" "public" {
  route_table_id = aws_route_table.public.id

  for_each  = aws_subnet.public
  subnet_id = each.value.id
}
