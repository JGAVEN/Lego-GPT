variable "project" {
  description = "GCP project ID"
}

variable "region" {
  description = "GCP region"
}

variable "zone" {
  description = "GCP zone"
}

variable "image" {
  description = "Base VM image"
}

variable "docker_image" {
  description = "Lego GPT Docker image"
}

variable "jwt_secret" {
  description = "JWT secret passed to the container"
  sensitive   = true
}
