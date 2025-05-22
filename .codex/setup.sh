#!/bin/bash
set -euo pipefail

# Update submodules
if [ -f .gitmodules ]; then
  git submodule update --init --recursive
fi

# Dependencies are assumed to be present in the Codex environment
echo "Skipping dependency installation (offline mode)"
