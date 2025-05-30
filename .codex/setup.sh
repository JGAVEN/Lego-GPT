#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Use Node version from .nvmrc when nvm is available
if command -v nvm >/dev/null 2>&1; then
  nvm install >/dev/null 2>&1 || true
  nvm use || true
fi

# Install backend dependencies (including test tools)
python -m pip install --no-cache-dir -e ./backend[test] || \
  echo "Warning: could not install Python packages"

# Enable pre-commit hooks if available
if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install || echo "Warning: pre-commit install failed"
fi

# Install pnpm for front-end package management
corepack enable
corepack prepare pnpm@10.5.2 --activate

# Install front-end packages using the project script. This populates the
# pnpm store and verifies the Cypress binary so future lints and tests work
# offline.
./scripts/setup_frontend.sh || \
  echo "Warning: front-end setup failed; linting may be skipped"
