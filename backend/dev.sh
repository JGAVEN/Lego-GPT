#!/bin/bash

# Simple dev helper running the FastAPI app
set -euo pipefail
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
