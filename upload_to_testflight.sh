#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$SCRIPT_DIR/tools/install_deps.sh"
python3 -m upload_to_testflight_cmd_entry "$@"
