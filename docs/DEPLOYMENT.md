# Deployment Guide

This document explains how to deploy Lego GPT in production.

## Docker Compose

The simplest way to run the stack is via Docker Compose:

```bash
docker compose up --build -d
```

This launches Redis, the API gateway and both worker processes.  Configure secrets in a `.env` file or pass them via the environment.

## Terraform

Sample Terraform templates live in `infrastructure/terraform`. Copy the directory for your cloud provider and set variables via `TF_VAR_` environment variables:

```bash
export TF_VAR_jwt_secret=$(openssl rand -hex 32)
export TF_VAR_docker_image=ghcr.io/<owner>/lego-gpt:v0.5.40
```

Run `terraform init` followed by `terraform apply` to provision the resources.

Keep secrets out of source control by relying on environment variables or dedicated secret stores.

## Best Practices

* Rotate the `JWT_SECRET` periodically (`docs/TOKEN_ROTATION.md`).
* Use HTTPS and restrict network access to Redis.
* Monitor worker logs and set up alerts for failed jobs.
* Benchmark changes regularly to catch performance regressions.
