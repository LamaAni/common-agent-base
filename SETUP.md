# SETUP.md — Workspace Setup Instructions
_Read by an LLM agent, not by the user. Execute each step in order._
_Non-interactive mode: if running without a user present, use dummy values where noted._

---

## Before you start

Tell the user:
> "I'm going to set up your workspace. I'll ask you some questions — just answer in plain English. This takes about 10 minutes."

Work through the steps below. Explain what you're doing in plain English as you go. Never show terminal output or code to the user.

---

## Step 1 — Prerequisites check

Check that the following are installed. For each one missing, give the user a plain-English install instruction with a link, and wait for their confirmation before continuing.

| Requirement | How to check | Install link |
|-------------|-------------|-------------|
| Python 3.10+ | `python3 --version` or `python --version` | [python.org/downloads](https://python.org/downloads) |
| git | `git --version` | [git-scm.com](https://git-scm.com) |
| Node.js 18+ | `node --version` | [nodejs.org](https://nodejs.org) |

---

## Step 2 — Interview

Ask every question below, one at a time, waiting for the answer before moving on.
Record all answers — you will use them to fill in `AGENT.md` and configure the workspace.

### A — Identity
1. "What should I call myself? This is the name I'll use when I introduce myself. (e.g. Aria, Max, Sage)"
2. "What's your name?"
3. "What company do you work at?"
4. "What's your team or department?"
5. "What's your role or title?"

### B — Work context
6. "What do you mainly use an assistant for? Pick everything that applies:
   - Summarising documents or reports
   - Drafting emails, memos, or communications
   - Analysing data from spreadsheets or databases
   - Research and competitive intelligence
   - Project and task tracking
   - Meeting prep or note-taking
   - Something else — tell me what"

7. "How do you prefer your outputs?
   - Short and direct — bullet points, executive summary, bottom line up front
   - Detailed and thorough — full context, all sections, complete analysis"

### C — Tools and integrations
8. "Which of these do you use regularly at work? Pick all that apply:
   - Slack
   - Google Drive, Docs, or Sheets
   - Microsoft SharePoint or OneDrive
   - Microsoft Teams
   - Notion
   - Outlook or Gmail
   - Excel or CSV files
   - PDF documents
   - PowerPoint or Google Slides
   - Something else — tell me what"

### D — MCP integrations (ask only if user is comfortable with optional setup)
Based on their answer to question 8, suggest relevant MCP connections:
- Slack selected -> "I can connect directly to Slack to read channels and send messages. Want me to set that up? You'll need a Slack bot token from api.slack.com."
- Google Drive selected -> "I can connect to Google Drive to read and write files directly. Want me to enable that?"
- Research/web mentioned -> "I can control a browser to research websites for you. Want me to enable that?"

For each MCP server the user wants, note it down. You will configure it in Step 6.
If the user is not sure, skip and note: "MCP integrations can be added anytime later."

---

## Step 3 — Create CLAUDE.md from AGENT.md

`AGENT.md` is the canonical template committed to the repo. `CLAUDE.md` is the personalised working copy that Claude Code loads automatically — it does not exist until setup runs.

Run from the repo root:
```
cp AGENT.md CLAUDE.md
```

Then replace every `[PLACEHOLDER]` in `CLAUDE.md` using the interview answers:

| Placeholder | Value |
|-------------|-------|
| `[AGENT_NAME]` | Answer to question 1 |
| `[USERNAME]` | Answer to question 2 |
| `[COMPANY_NAME]` | Answer to question 3 |
| `[TEAM_NAME]` | Answer to question 4 |
| `[USER_ROLE]` | Answer to question 5 |
| `[SETUP_DATE]` | Today's date (YYYY-MM-DD) |
| `[PRIMARY_USE_CASES]` | Answer to question 6 (comma-separated) |
| `[OUTPUT_PREFERENCE]` | Answer to question 7 |
| `[TOOLS_USED]` | Answer to question 8 (comma-separated) |
| `[FILE_FORMATS]` | File types mentioned in question 8 |

Also replace `[AGENT_NAME]` in `README.md`.

Commit: `config: personalisation complete — agent named [AGENT_NAME]`

---

## Step 4 — Secrets setup

Copy `.env.example` to `.env`.

For each key in `.env.example`, ask the user in plain English what the value is and where to find it. Fill in any they provide. Leave blank any they do not have yet — they can add them later.

Tell the user: "You can add more keys to `.env` any time as you connect new services."

---

## Step 5 — Python environment

**Sub-step 5a — Create venv (always run this, regardless of what comes next):**

Run from the repo root:
```
python3 -m venv .agent/.venv
```
On Windows: `python -m venv .agent\.venv`

**Sub-step 5b — Install packages (only if requirements.txt has content):**

Check whether `.agent/setup/requirements.txt` exists and has content (not just a `.gitkeep`).
If yes:
```
.agent/.venv/bin/python -m pip install -r .agent/setup/requirements.txt
```
On Windows: `.agent\.venv\Scripts\python.exe -m pip install -r .agent\setup\requirements.txt`

If no: skip 5b and note it as pending.

---

## Step 6 — MCP configuration

Create `.agent/mcp/config.json` with the servers the user selected in Step 2D.

Base template:
```json
{
  "mcpServers": {}
}
```

Add blocks for each selected integration:

**Browser (research/web):**
```json
"browser": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"],
  "_note": "Browser automation — navigate, extract, screenshot any website"
}
```

**Slack:**
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" },
  "_note": "Read channels, send messages"
}
```

**Google Drive:**
```json
"gdrive": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gdrive"],
  "_note": "Read and write Google Drive files"
}
```

If no servers selected: write `config.json` with empty `mcpServers: {}`.

Then wire `.mcp.json`. Run from the repo root:

**macOS/Linux:**
```
ln -s .agent/mcp/config.json .mcp.json
```

**If symlink fails (Windows default):**
```
cp .agent/mcp/config.json .mcp.json
```
Note for Windows users: re-run this copy whenever `.agent/mcp/config.json` changes.

For any MCP server added, trigger first-time install:
```
npx [package]@latest --help
```
If `npx` is unavailable, give the Node.js install link and wait.

Commit: `config: MCP configured — [list servers, or "none selected"]`

---

## Step 7 — Commands wiring

Run from the repo root:

**macOS/Linux:**
```
ln -s ../.agent/commands .claude/commands
```

**If symlink fails (Windows default):**
Copy all `.md` files from `.agent/commands/` into `.claude/commands/`.
Note: re-run this copy whenever commands are added or changed.

If `.agent/commands/` has only a `.gitkeep`: create the symlink/directory anyway — commands will populate in a future update.

Commit: `config: commands wired`

---

## Step 8 — Memory bootstrap

Use the platform's memory tools to create the following. Do not write to a hardcoded path — the platform manages the memory directory automatically.

**Memory index:**
```
# Memory Index

- [User Profile](user_profile.md) — [USERNAME]'s role, context, and preferences
```

**User profile (`user_profile.md`):**
```
Name: [USERNAME]
Company: [COMPANY_NAME]
Team: [TEAM_NAME]
Role: [USER_ROLE]
Primary use cases: [PRIMARY_USE_CASES]
Output preference: [OUTPUT_PREFERENCE]
Tools used: [TOOLS_USED]
Prefers: plain English, outcomes not methods, no jargon
```

---

## Step 9 — Verification

Run from the repo root:
```
python .agent/tools/cli.py --help
```

If it prints a list of commands without errors: verification passed.
If `.agent/tools/cli.py` does not exist yet: note as pending, do not fail setup.

---

## Step 10 — Restart

Build the summary dynamically from what actually happened in steps 1-9. Then tell the user:

> "Setup is complete. **Please close this conversation and open a new one.** In the new session I'll introduce myself as [AGENT_NAME] and I'll already know your context.
>
> **What's ready now:** [list completed steps in plain English]
>
> **Coming in future updates:** [list skipped steps with plain-English reason]
>
> You can already ask me to write documents, summaries, analyses, draft emails, or any other task — I'll organise everything in your **Work/** folder by project."
