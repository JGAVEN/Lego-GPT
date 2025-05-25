#!/bin/bash
# Install Docker if missing
if ! command -v docker >/dev/null; then
  apt-get update && apt-get install -y docker.io
fi
# Run Lego GPT container
docker run -d -p 8000:8000 \
  -e JWT_SECRET=${jwt_secret} \
  ${image}
