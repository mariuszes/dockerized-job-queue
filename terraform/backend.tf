terraform {
  backend "s3" {
    bucket       = "job-queue-tfstate-636993912104"
    key          = "job-queue/terraform.tfstate"
    region       = "eu-central-1"
    use_lockfile = true
  }
}
