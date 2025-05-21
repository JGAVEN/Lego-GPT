#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Install pip and Poetry
pip install --upgrade pip
pip install poetry

# Install Python dependencies for the backend
poetry install --no-interaction --no-root

# Install frontend dependencies
if [ -d "frontend" ]; then
  cd frontend
  pnpm install
  cd ..
fi

# Run backend tests if pytest is available
if command -v pytest >/dev/null 2>&1; then
  poetry run pytest -q || true
fi
