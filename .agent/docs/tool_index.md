# Tool Index

Check this before writing any new tool. If a match exists, use it. If close, extend it.

| Command | Directory | What it does | Input | Output |
|---------|-----------|-------------|-------|--------|
| `install` | `.agent/tools/cli.py` | Full install: MCP stub + all symlinks | — | Status lines |
| `sync-links` | `.agent/tools/cli.py` | Re-wire all symlinks from YAML | `--dry-run` flag | Status lines |
| `sync_links` | `.agent/tools/sync_links/sync_links.py` | Core link logic (used by CLI) | `config_path`, `dry_run` | `list[str]` |

