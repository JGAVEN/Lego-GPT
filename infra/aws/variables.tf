variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "api_image" {
  description = "Container image for the API server"
  type        = string
}

variable "redis_url" {
  description = "Redis connection URL"
  type        = string
}

variable "jwt_secret" {
  description = "JWT secret for the API"
  type        = string
  sensitive   = true
}
