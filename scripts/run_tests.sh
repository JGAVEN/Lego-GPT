#!/bin/bash
set -euo pipefail
ruff check backend detector
python -m pytest -q
