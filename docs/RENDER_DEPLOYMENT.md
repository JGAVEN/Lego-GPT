# Render Deployment Guide

This guide explains how to deploy Lego GPT to [Render](https://render.com) using the bundled `render.yaml` blueprint. The interface is English only.

## Prerequisites

- A Render account
- Python 3.11 or newer
- Node.js 20 with `pnpm`
- A Redis instance (created automatically by the blueprint)

## Steps

1. Clone the repository and switch to the project root.
2. Apply the blueprint:

   ```bash
   render blueprint apply render.yaml
   ```

3. Update any secrets or environment variables through the Render dashboard or via `envVarGroups`. Common options include setting `JWT_SECRET` for API authentication, tweaking `RATE_LIMIT`, defining `VITE_API_URL` for the front-end (e.g. `https://lego-gpt-api-green.onrender.com`), and supplying a custom `LEGOGPT_MODEL` path if you host a larger checkpoint.
4. The blueprint sets up two API services:
   - `lego-gpt-api-green` (active)
   - `lego-gpt-api-blue` (disabled for blue/green rollouts)
5. A Redis instance and a static site for the front-end are provisioned automatically. The static site uses Node 20 during the build.
6. Visit `/docs` on the API service URL to view the OpenAPI specification. Admin users can fetch `/metrics_prom` for Prometheus metrics.

## Rolling Updates

To perform a blue/green deployment:

1. Enable the `lego-gpt-api-blue` service and wait for it to become healthy.
2. Disable `lego-gpt-api-green` once the blue service is serving traffic successfully.
3. Repeat the process for future updates, alternating between the two services.

