# Workspace Design — Internal Reference

Internal notes for any agent working in this repo. Read this if you're unsure how something is structured or why.

---

## Zone map

| Folder | Owner | User touches it? |
|--------|-------|-----------------|
| `Work/` | Agent writes, user reads | Yes — find results here |
| `README.md`, `SETUP.md` | Template | Yes — user reads README only |
| `.agent/` | Agent internal | No |
| `.claude/` | Platform config | No |
| `.cache/` | Runtime/temp, gitignored | No |

---

## Key conventions

**AGENT.md is the constitution**
SETUP.md fills placeholders directly into `AGENT.md`. `CLAUDE.md` is a runtime symlink to `AGENT.md` — created by `install.sh`, gitignored. Claude Code auto-loads `CLAUDE.md`. Never manually create or commit `CLAUDE.md`.

**`.agent/` is the canonical source**
All commands, tools, MCP config, and docs live in `.agent/`. Platform dirs (`.claude/`) symlink or copy from `.agent/` — never the reverse. Update `.agent/`, platforms follow.

**Runtime symlinks** are defined in `.agent/setup/shared_agent_config_symlinks.yaml` and created by `install.sh` / `cli.py install`. All are gitignored. Current links:
- `CLAUDE.md → AGENT.md`
- `.claude/commands → .agent/commands`
- `.mcp.json → .agent/mcp/config.json`

**Work/ is flat by default**
No pre-imposed subfolder taxonomy. Agent creates project folders dynamically using the order rules in `AGENT.md`. One folder per topic/project, named as `topic-slug/`.

**Index discipline**
Every folder with documents has an `INDEX.md`. The agent updates it immediately after creating any file. `Work/INDEX.md` maps projects; `Work/[project]/INDEX.md` maps files within. Never create a file without updating the index.

**Tool gate**
Before writing any Python tool, check `.agent/docs/tool_index.md`. If a match exists, use it. Only create new if nothing matches.

---

## Known gaps

- Memory is platform-tethered — switching AI platforms loses memory
- On Windows copy-fallback, new commands added to `.agent/commands/` need `cli.py sync-links` to appear in `.claude/commands/`
- `.env` has no rotation or per-environment management
- No scheduled/recurring tasks
- Binary outputs in `Work/` accumulate in git (no Git LFS configured)
- Corporate proxies may block PyPI/npm during install
