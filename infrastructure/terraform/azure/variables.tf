variable "location" {
  description = "Azure region"
}

variable "docker_image" {
  description = "Lego GPT Docker image"
}

variable "jwt_secret" {
  description = "JWT secret passed to the container"
  sensitive   = true
}
