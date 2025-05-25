variable "region" {
  description = "AWS region"
}

variable "ami" {
  description = "AMI ID for the instance"
}

variable "docker_image" {
  description = "Lego GPT Docker image"
}

variable "jwt_secret" {
  description = "JWT secret passed to the container"
  sensitive   = true
}
