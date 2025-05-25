# Infrastructure Samples

Terraform templates for deploying Lego GPT to cloud providers.

- `aws/` – deploys the API using AWS App Runner.

Each template expects an existing Redis instance and a container image published to a registry.
Secrets are supplied via environment variables to avoid storing them in the codebase.
