# Tool Index

Check this before writing any new tool. If a match exists, use it. If close, extend it.

| Command | Location | What it does | Key options | Output |
|---------|----------|-------------|-------------|--------|
| `install` | `.agent/tools/cli.py` | Full install: MCP stub + all symlinks | — | Status lines |
| `sync-links` | `.agent/tools/cli.py` | Re-wire all symlinks from YAML | `--dry-run` | Status lines |
| `index add` | `.agent/tools/cli.py` | Add or update an entry in `.agent/index.json` | `--path --type --about --use` | Status line |
| `index remove` | `.agent/tools/cli.py` | Remove an entry by path | `--path` | Status line |
| `index search` | `.agent/tools/cli.py` | Regex search across path, about, use | `PATTERN` | Matching entries |
| `index print` | `.agent/tools/cli.py` | Print full index in compact format | `--type` filter | Compact lines + token count |
| `index delta` | `.agent/tools/cli.py` | Show entries added since a datetime | `--since ISO8601` | New entries only |
| `sync_links` | `.agent/tools/sync_links/sync_links.py` | Core link logic (used by CLI) | `config_path`, `dry_run` | `list[str]` |
| `index_manager` | `.agent/tools/index_manager/index_manager.py` | Core index logic (used by CLI) | various | varies |

