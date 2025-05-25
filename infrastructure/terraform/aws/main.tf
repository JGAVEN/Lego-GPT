terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = var.region
}

resource "aws_instance" "lego_gpt" {
  ami           = var.ami
  instance_type = "t3.micro"
  user_data     = templatefile("${path.module}/user-data.sh", {
    image      = var.docker_image
    jwt_secret = var.jwt_secret
  })
}
