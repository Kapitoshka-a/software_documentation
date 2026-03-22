#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CSV_PATH="$ROOT_DIR/chat_data.csv"

export PYTHONPATH="$ROOT_DIR"

python "$ROOT_DIR/scripts/generate_mock_data.py" --rows 1000 --output "$CSV_PATH"
python "$ROOT_DIR/scripts/import_data.py" --csv "$CSV_PATH"
