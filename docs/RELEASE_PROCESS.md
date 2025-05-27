# Community Release Process

> **Note**: Lego GPT is maintained in English only.

This guide explains how to cut a new release tag and publish Docker images.

1. Ensure `CHANGELOG.md` lists all notable changes.
2. Run the test suite: `./scripts/run_tests.sh`.
3. Commit your updates:
   ```bash
   git commit -am "chore: prepare release"
   ```
4. Create an annotated tag matching the new version:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```
5. GitHub Actions runs `.github/workflows/release.yml` which bumps
   the version, commits it back to `main` and builds the Docker images.
6. Once the workflow completes, pull the images from GitHub Container Registry:
   ```bash
   docker pull ghcr.io/<owner>/lego-gpt:vX.Y.Z
   docker pull ghcr.io/<owner>/lego-gpt:gpu-vX.Y.Z
   ```
