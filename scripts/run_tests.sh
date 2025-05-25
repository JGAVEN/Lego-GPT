#!/bin/bash
set -euo pipefail
ruff check backend detector
python -m pytest -q
if [ -x frontend/node_modules/.bin/cypress ]; then
  pnpm --dir frontend exec cypress run
else
  echo "Cypress not installed; skipping UI tests." >&2
fi
