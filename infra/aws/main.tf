terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_apprunner_service" "lego_gpt" {
  service_name = "lego-gpt-api"

  source_configuration {
    image_repository {
      image_identifier      = var.api_image
      image_repository_type = "ECR_PUBLIC"
      image_configuration {
        port = "8000"
        runtime_environment_variables = {
          REDIS_URL  = var.redis_url
          JWT_SECRET = var.jwt_secret
        }
      }
    }
    auto_deployments_enabled = true
  }
}
