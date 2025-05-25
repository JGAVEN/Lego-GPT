terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "lego_gpt" {
  name     = "lego-gpt-rg"
  location = var.location
}

resource "azurerm_container_group" "lego_gpt" {
  name                = "lego-gpt"
  location            = azurerm_resource_group.lego_gpt.location
  resource_group_name = azurerm_resource_group.lego_gpt.name
  os_type             = "Linux"
  ip_address_type     = "public"

  container {
    name   = "lego-gpt"
    image  = var.docker_image
    cpu    = "1"
    memory = "1.5"
    ports {
      port     = 8000
      protocol = "TCP"
    }
    environment_variables = {
      JWT_SECRET = var.jwt_secret
    }
  }
}
