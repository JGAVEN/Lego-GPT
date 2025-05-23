#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Install Python dependencies before network access is disabled
python -m pip install --no-cache-dir ortools redis rq

# Pre-fetch front-end packages while network access is available
pnpm fetch --prod=false --dir frontend
# Install using the cached packages once network access is removed
pnpm install --offline --dir frontend
