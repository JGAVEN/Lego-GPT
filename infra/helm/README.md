# Lego GPT Helm Chart

This chart provides a simple way to deploy Lego GPT on Kubernetes using Helm.
It mirrors the manifests in `../k8s` but exposes a few configurable values.

## Usage

```bash
helm install lego-gpt infra/helm \
  --set image.repository=ghcr.io/<owner>/lego-gpt \
  --set image.tag=v0.5.62
```

The chart deploys the API, worker and detector deployments along with Redis.
Adjust the values file or `--set` flags to suit your environment.
