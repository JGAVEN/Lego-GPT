#!/usr/bin/env bash
# Fetch and install front-end dependencies.
# Run with network access during initial setup.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT/frontend"

# Attempt offline install first. If packages are missing, fall back to
# fetching them from the registry (requires network) and reinstall
# from the local store.
if pnpm install --offline; then
  echo "Front-end dependencies installed from offline store."
  exit 0
fi

echo "Offline install failed – fetching packages from registry..."
if curl -I --max-time 5 https://registry.npmjs.org >/dev/null 2>&1; then
  pnpm fetch --prod=false
  pnpm install --offline
  echo "Front-end dependencies installed."
else
  echo "Network unavailable. Connect to the internet and re-run this script." >&2
  exit 1
fi
