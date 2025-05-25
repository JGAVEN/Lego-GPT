#!/bin/bash
set -euo pipefail
ruff check backend detector
python -m pytest -q

# Ensure front-end dependencies are available for Cypress tests and linting.
if [ ! -x frontend/node_modules/.bin/eslint ]; then
  ./scripts/setup_frontend.sh || true
fi

if [ -x frontend/node_modules/.bin/cypress ]; then
  pnpm --dir frontend exec cypress run
else
  echo "Cypress not installed; skipping UI tests." >&2
fi
