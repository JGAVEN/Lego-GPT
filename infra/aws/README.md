# AWS Terraform Sample

This folder contains a minimal Terraform configuration for deploying the Lego GPT API to [AWS App Runner](https://aws.amazon.com/apprunner/).
It expects a container image published to a registry such as GitHub Container Registry or Amazon ECR Public.

## Prerequisites
- Terraform 1.5 or newer
- AWS credentials exported as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

## Usage
1. Export the required variables:
   ```bash
   export TF_VAR_api_image=ghcr.io/<owner>/lego-gpt:v0.5.38
   export TF_VAR_redis_url=redis://hostname:6379/0
   export TF_VAR_jwt_secret=$(openssl rand -hex 32)
   # Optional: region, defaults to us-east-1
   export TF_VAR_region=us-east-1
   ```
2. Initialise and apply the plan:
   ```bash
   terraform init
   terraform apply
   ```

Secrets are provided via `TF_VAR_` environment variables so they do not need to be committed to version control.
You can also create a `terraform.tfvars` file if preferred.
For team usage configure remote state (for example via an S3 backend) so each
`terraform apply` uses the same state file. Adjust the variables in
[`variables.tf`](variables.tf) to customise the App Runner service name or
region. Refer to the Terraform documentation for tuning memory and CPU
requirements.
