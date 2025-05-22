#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Install OR-Tools before network access is disabled
python -m pip install --no-cache-dir ortools
