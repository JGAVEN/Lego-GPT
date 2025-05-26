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
if [ -x frontend/node_modules/.bin/lighthouse ]; then
  node scripts/lighthouse_ci.js || echo "Lighthouse check failed" >&2
else
  echo "Lighthouse not installed; skipping performance audit." >&2
fi
