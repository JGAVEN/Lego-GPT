#!/usr/bin/env bash
# Fetch and install front-end dependencies.
# Run with network access during initial setup.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
# Fetch packages to pnpm store
pnpm fetch --prod=false --dir "$REPO_ROOT/frontend"
# Install dependencies using offline store
pnpm install --offline --dir "$REPO_ROOT/frontend"
echo "Front-end dependencies installed."
