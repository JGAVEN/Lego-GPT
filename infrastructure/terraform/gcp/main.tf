terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_compute_instance" "lego_gpt" {
  name         = "lego-gpt"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  metadata_startup_script = templatefile("${path.module}/startup.sh", {
    image      = var.docker_image
    jwt_secret = var.jwt_secret
  })
}
