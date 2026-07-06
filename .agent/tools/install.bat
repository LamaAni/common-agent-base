@echo off
cd /d "%~dp0..\.."
python -m venv .agent\.venv
.agent\.venv\Scripts\pip install -q -r .agent\setup\requirements.txt
.agent\.venv\Scripts\python .agent\tools\cli.py install
