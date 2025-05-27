# Kubernetes Sample

> **Note**: The provided Kubernetes manifests assume the application is English-only.

This folder provides a minimal set of manifests for running Lego GPT on Kubernetes. The manifests assume a container image is already available in a registry and that all services can share a Redis instance within the cluster.

## Usage

1. Edit `lego-gpt.yaml` and replace `ghcr.io/<owner>/lego-gpt:v0.5.61` with your published image.
2. Create a secret for the JWT signing key:
   ```bash
   kubectl create secret generic lego-gpt-secret --from-literal=jwt-secret=<your secret>
   ```
3. Apply the resources:
   ```bash
   kubectl apply -f lego-gpt.yaml
   ```
4. Expose the API service using a LoadBalancer or Ingress as appropriate for your cluster.

These manifests are intended as a starting point for development or small deployments. Adjust resource requests, replica counts and ingress configuration to suit your environment.
