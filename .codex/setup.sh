#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Install backend dependencies (including fakeredis for tests)
python -m pip install --no-cache-dir -e ./backend[test] || \
  echo "Warning: could not install Python packages"

# Install pnpm for front-end package management
corepack enable
corepack prepare pnpm@10.5.2 --activate

# Pre-fetch front-end packages while network access is available
pnpm fetch --prod=false --dir frontend
# Install using the cached packages once network access is removed
pnpm install --offline --dir frontend
