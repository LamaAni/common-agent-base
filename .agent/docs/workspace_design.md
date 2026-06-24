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

**AGENT.md → CLAUDE.md**
`AGENT.md` is the committed template. `CLAUDE.md` does not exist until SETUP.md runs — it is created by `cp AGENT.md CLAUDE.md` and personalised in-place. Claude Code auto-loads `CLAUDE.md`. Never commit `CLAUDE.md` to the template repo.

**`.agent/` is the canonical source**
All commands, tools, MCP config, and docs live in `.agent/`. Platform dirs (`.claude/`) symlink or copy from `.agent/` — never the reverse. Update `.agent/`, platforms follow.

**Work/ is flat by default**
No pre-imposed subfolder taxonomy. Agent creates project folders dynamically using the order rules in `CLAUDE.md`. One folder per topic/project, named as `topic-slug/`.

**Index discipline**
Every folder with documents has an `INDEX.md`. The agent updates it immediately after creating any file. `Work/INDEX.md` maps projects; `Work/[project]/INDEX.md` maps files within. Never create a file without updating the index.

**Tool gate**
Before writing any Python tool, check `.agent/docs/tool_index.md`. If a match exists, use it. Only create new if nothing matches.

---

## Known gaps (as of v0.1)

- Memory is platform-tethered — switching AI platforms loses memory
- Commands symlink doesn't auto-extend to non-Claude platforms
- `.env` has no rotation or per-environment management
- No scheduled/recurring tasks
- No session resume for interrupted long tasks
- Binary outputs in `Work/` accumulate in git (no Git LFS configured)
- Corporate proxies may block PyPI/npm during setup
