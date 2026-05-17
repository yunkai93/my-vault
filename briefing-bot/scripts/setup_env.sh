#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/wuchao/ai/my-vault/briefing-bot"
VENV="$ROOT/.venv"

python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r "$ROOT/requirements.txt"
