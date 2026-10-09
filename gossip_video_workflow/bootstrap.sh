#!/usr/bin/env bash
set -euo pipefail
workflow_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for tool in python3 node npm ffmpeg ffprobe; do command -v "$tool" >/dev/null || { echo "Missing cloud dependency: $tool"; exit 1; }; done
python3 -m venv "$workflow_dir/.venv"
"$workflow_dir/.venv/bin/python" -m pip install --upgrade pip
"$workflow_dir/.venv/bin/python" -m pip install 'torch==2.6.0' --index-url https://download.pytorch.org/whl/cpu
"$workflow_dir/.venv/bin/python" -m pip install -r "$workflow_dir/requirements.txt"
(cd "$workflow_dir/runtime" && npm ci --ignore-scripts)
"$workflow_dir/.venv/bin/python" "$workflow_dir/install_browser.py"
echo 'Cloud video runtime ready. No user-PC model or paid TTS key required.'
