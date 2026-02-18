#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "$ROOT_DIR/.gitmodules" ]; then
  echo "ERROR: .gitmodules found. Python dependencies must not use git submodules."
  exit 1
fi

if git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if git -C "$ROOT_DIR" submodule status --recursive 2>/dev/null | grep -q .; then
    echo "ERROR: git submodules detected. Python dependencies must be installed via pyproject git refs."
    exit 1
  fi
fi

echo "No git submodules detected."
