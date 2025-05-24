#!/usr/bin/env bash
# Fetch and install front-end dependencies.
# Run with network access during initial setup.
# Installs React runtime packages and dev tools used by lint_frontend.js:
#   @eslint/js, @types/react, @types/react-dom, @vitejs/plugin-react,
#   eslint, eslint-config-prettier, eslint-plugin-react-hooks,
#   eslint-plugin-react-refresh, globals, prettier, typescript,
#   typescript-eslint and vite.
set -euo pipefail

if ! command -v pnpm >/dev/null 2>&1; then
  echo "pnpm is required. Install it first (see README.md)." >&2
  exit 1
fi
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

echo "Offline install failed – attempting to fetch packages from registry..."
if curl -I --max-time 5 https://registry.npmjs.org >/dev/null 2>&1; then
  pnpm fetch --prod=false
  pnpm install --offline
  echo "Front-end dependencies installed."
  exit 0
fi

cat >&2 <<'EOF'
Network unavailable and the pnpm store is missing required packages.
Run this script once with network access to populate the store.
See README.md for details.
EOF
exit 1
