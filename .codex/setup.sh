#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Install Python dependencies for the backend
poetry install --no-interaction --no-root

# Install frontend dependencies
if [ -d "frontend" ]; then
  cd frontend
  pnpm install
  cd ..
fi
