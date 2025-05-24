#!/usr/bin/env bash
# Build and run the detector training container.
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: train_detector.sh <data.yaml> [additional args]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_PATH="$1"
shift

docker build -f "$ROOT_DIR/detector/Dockerfile.train" -t lego-detect-train "$ROOT_DIR"
DATA_DIR="$(dirname "$DATA_PATH")"
DATA_FILE="$(basename "$DATA_PATH")"
docker run --rm -v "${DATA_DIR}:/data" lego-detect-train lego-detect-train "/data/${DATA_FILE}" "$@"
