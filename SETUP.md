# SETUP.md — Workspace Setup Instructions
_Read by an LLM agent, not by the user. Execute each step in order._

---

## Before you start

Tell the user:
> "I'm going to set up your workspace. I'll ask you a few questions — just answer in plain English."

Then work through the steps below. Explain what you're doing in plain English as you go. Never show terminal output or code to the user.

---

## Step 1 — Prerequisites check

Check that the following are installed. For each one missing, give the user a plain-English install instruction with a link, and wait for confirmation before continuing.

| Requirement | How to check | Install link |
|-------------|-------------|-------------|
| Python 3.10+ | `python3 --version` or `python --version` | [python.org/downloads](https://python.org/downloads) |
| git | `git --version` | [git-scm.com](https://git-scm.com) |
| Node.js 18+ | `node --version` | [nodejs.org](https://nodejs.org) |

---

## Step 2 — Personalization

Ask the user these questions one at a time. Wait for each answer before asking the next.

1. "What should I call myself? (e.g. Aria, Max, Sage — pick any name you like)"
2. "What's your name?"
3. "What company do you work at?"
4. "What's your team or department?"
5. "What's your role or title?"

Once you have all answers, replace every `[PLACEHOLDER]` in `CLAUDE.md` and `README.md`:

| Placeholder | Answer from |
|-------------|------------|
| `[AGENT_NAME]` | Question 1 |
| `[USERNAME]` | Question 2 |
| `[COMPANY_NAME]` | Question 3 |
| `[TEAM_NAME]` | Question 4 |
| `[USER_ROLE]` | Question 5 |
| `[SETUP_DATE]` | Today's date (YYYY-MM-DD) |

Commit: `config: personalization complete — agent named [AGENT_NAME]`

---

## Step 3 — Secrets setup

Copy `.env.example` to `.env`.

For each key in `.env.example`, ask the user in plain English what the value is and where to get it. Fill in the values they provide. Leave blank any they don't have yet.

Tell the user: "You can add more keys to `.env` later as you connect new services."

---

## Step 4 — Python environment

Run:
```
python3 -m venv .agent/.venv
```

Then install packages:
```
.agent/.venv/bin/python -m pip install -r .agent/setup/requirements.txt
```

On Windows, replace `.agent/.venv/bin/python` with `.agent\.venv\Scripts\python.exe`.

If `requirements.txt` does not exist yet, skip this step and tell the user:
> "The Python tools are still being built. I'll set them up when they're ready."

---

## Step 5 — Commands wiring

Wire `.claude/commands/` to `.agent/commands/` so slash commands work.

**Try symlink first (macOS/Linux):**
```
ln -s ../.agent/commands .claude/commands
```

**If symlink fails (Windows default):**
Copy the contents of `.agent/commands/` into `.claude/commands/`. Run `.agent/run.bat sync-commands` any time commands are added or changed.

If `.agent/run.bat` does not exist yet, skip the sync step — commands will be wired manually in a later update.

---

## Step 6 — MCP wiring

Wire `.mcp.json` to `.agent/mcp/config.json`.

**Try symlink first (macOS/Linux):**
```
ln -s .agent/mcp/config.json .mcp.json
```

**If symlink fails:**
Copy `.agent/mcp/config.json` to `.mcp.json`.

If `.agent/mcp/config.json` does not exist yet, skip this step.

---

## Step 7 — Memory bootstrap

Create a memory file for the user. Write it to the platform's memory directory (Claude Code manages this path automatically when you use the memory tools).

Seed it with:
```
# Memory Index

- [User Profile](user_profile.md) — [USERNAME]'s role, preferences, and background
```

Then create `user_profile.md` in the same directory with:
```
Name: [USERNAME]
Company: [COMPANY_NAME]
Team: [TEAM_NAME]
Role: [USER_ROLE]
Prefers: plain English, no jargon, outcomes not methods
```

---

## Step 8 — Verification

Run `python .agent/tools/cli.py --help` and confirm it prints a list of commands without errors.

If `.agent/tools/cli.py` does not exist yet, skip and tell the user:
> "The tool runner will be verified in the next update."

---

## Step 9 — Restart

Tell the user:

> "Setup is complete. **Please close this conversation and open a new one.** Your assistant's name and settings will be active in the new session.
>
> **Known limitations at this stage:**
> - The Python tool runner is not yet installed (coming in the next update)
> - MCP browser tool is not yet configured (coming in the next update)
>
> You can already ask me to write documents, summaries, analyses, or any other task — I'll organise everything in your **Work/** folder."
