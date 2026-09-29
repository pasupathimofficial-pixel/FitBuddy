#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PYTHON="$(command -v python3 || command -v python)"
if [ -z "$PYTHON" ]; then
  echo "Python 3.10+ is required."
  exit 1
fi
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -m venv .venv
fi
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python launcher.py
