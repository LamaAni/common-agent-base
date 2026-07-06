#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../.."   # repo root

python3 -m venv .agent/.venv
.agent/.venv/bin/pip install -q -r .agent/setup/requirements.txt
.agent/.venv/bin/python .agent/tools/cli.py install
