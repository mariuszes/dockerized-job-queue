resource "aws_s3_bucket" "terraform_state" {
  bucket = "job-queue-tfstate-636993912104"

  tags = {
    Name = "job-queue-tfstate"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}
