module "network" {
  source = "./modules/network"

  vpc_cidr = "10.0.0.0/16"

  public_subnets = {
    public-a = {
      cidr = "10.0.1.0/24"
      az   = "eu-central-1a"
    }

    public-b = {
      cidr = "10.0.2.0/24"
      az   = "eu-central-1b"
    }
  }
}

module "eks" {
  source = "./modules/eks"

  cluster_name       = "job-queue"
  subnet_ids         = module.network.public_subnet_ids
  kubernetes_version = "1.36"

  instance_type = "c7i-flex.large"
  min_size      = 1
  desired_size  = 2
  max_size      = 2
}

module "app_aws" {
  source = "./modules/app_aws"

  cluster_name = module.eks.cluster_name
}