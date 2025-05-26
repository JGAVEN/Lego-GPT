# Infrastructure Samples

Terraform templates for deploying Lego GPT to cloud providers.

- `aws/` – deploys the API using AWS App Runner.
- `k8s/` – sample manifests for running the stack on Kubernetes.

Each template expects an existing Redis instance and a container image published
to a registry. Secrets are supplied via environment variables to avoid storing
them in the codebase. You can also place them in a `terraform.tfvars` file.
For production deployments configure remote state (e.g. S3) so the state file
is shared across your team.
