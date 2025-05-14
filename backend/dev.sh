#!/bin/zsh

# Install dependencies if needed
poetry install --no-root

# Run the dev server
poetry run uvicorn api:app --reload
