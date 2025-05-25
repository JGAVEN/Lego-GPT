# Terraform Templates

Sample Terraform configurations for deploying Lego GPT on various cloud providers.
These templates are intentionally minimal and use environment variables for sensitive values.
Copy the appropriate directory, set the required variables, and run `terraform init && terraform apply`.

## Secrets via Environment Variables
Terraform automatically picks up variables prefixed with `TF_VAR_`.
Export the following before applying the plan:

```bash
export TF_VAR_jwt_secret=mysecret
export TF_VAR_docker_image=ghcr.io/<owner>/lego-gpt:latest
# Provider credentials
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

Refer to each provider directory for details.
