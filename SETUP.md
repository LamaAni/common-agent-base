# SETUP.md — Workspace Setup Instructions
_Read by an LLM agent, not by the user. Execute each step in order._
_Non-interactive mode: if running without a user present, use dummy values where noted._

---

## Before you start

Tell the user:
> "I'm going to set up your workspace. I'll ask you some questions — just answer in plain English. This takes about 10 minutes."

Work through the steps below. Explain what you're doing in plain English as you go. Never show terminal output or code to the user.

---

## Step 1 — Prerequisites

First, detect the user's operating system by running `uname -s` (Linux/macOS) or checking `%OS%` (Windows). Use this throughout to give OS-appropriate instructions.

Handle each prerequisite below in order. For each one: check silently, then either confirm it's ready or walk the user through installing it. **Do not move to the next prerequisite until the current one is confirmed working.**

---

### 1a — Python

Check: `python3 --version` (or `python --version` on Windows).

**If Python 3.10 or higher is found:** Tell the user "Python is ready." Move on.

**If Python is missing or older than 3.10:** Tell the user:

> "I need to install Python — it's the engine that runs your assistant's tools. Here's how:
>
> **Windows:**
> 1. Go to [python.org/downloads](https://python.org/downloads) — click the big yellow "Download Python" button
> 2. Run the file you downloaded
> 3. On the first screen, tick the box that says **"Add Python to PATH"** — this is important, don't skip it
> 4. Click "Install Now" and wait for it to finish
> 5. Come back here and tell me when it's done
>
> **Mac:**
> 1. Go to [python.org/downloads](https://python.org/downloads) — click the big yellow "Download Python" button
> 2. Open the downloaded file and follow the installer steps
> 3. Come back here and tell me when it's done
>
> **Linux:**
> 1. Open a terminal and run: `sudo apt install python3` (Ubuntu/Debian) or `sudo dnf install python3` (Fedora)
> 2. Come back here and tell me when it's done"

Wait for the user to confirm. Then re-check `python3 --version`. If it still fails, help the user troubleshoot — common issues: forgot to tick "Add to PATH" on Windows (fix: re-run installer and tick it), or needs to restart the terminal. Do not proceed until Python works.

---

### 1b — git

Check: `git --version`.

**If git is found:** Tell the user "git is ready." Move on.

**If git is missing:** Tell the user:

> "I need to install git — it keeps backups of everything your assistant produces. Here's how:
>
> **Windows:**
> 1. Go to [git-scm.com/download/win](https://git-scm.com/download/win) — the download will start automatically
> 2. Run the installer and click Next on every screen — the defaults are all fine
> 3. Come back here and tell me when it's done
>
> **Mac:**
> 1. Open the Terminal app (search for "Terminal" in Spotlight)
> 2. Type `xcode-select --install` and press Enter
> 3. Click Install in the window that appears and wait for it to finish
> 4. Come back here and tell me when it's done
>
> **Linux:**
> 1. Run: `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora)
> 2. Come back here and tell me when it's done"

Wait for confirmation. Re-check `git --version`. Do not proceed until git works.

---

### 1c — Node.js

Check: `node --version`.

**If Node.js 18 or higher is found:** Tell the user "Node.js is ready." Move on.

**If Node.js is missing or older than 18:** Tell the user:

> "I need to install Node.js — it runs the connectors that let your assistant talk to tools like Slack and Google Drive. Here's how:
>
> **Windows and Mac:**
> 1. Go to [nodejs.org](https://nodejs.org) — click the button that says **"LTS"** (that's the stable version)
> 2. Run the downloaded installer and click Next on every screen — the defaults are all fine
> 3. Come back here and tell me when it's done
>
> **Linux:**
> 1. Run: `sudo apt install nodejs npm` (Ubuntu/Debian) or `sudo dnf install nodejs` (Fedora)
> 2. Come back here and tell me when it's done"

Wait for confirmation. Re-check `node --version`. Do not proceed until Node.js 18+ works.

---

Once all three are confirmed, tell the user: "Great — everything is installed. Let's set up your assistant now."

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

For any MCP server added, trigger first-time install:
```
npx [package]@latest --help
```
If `npx` is unavailable, give the Node.js install link and wait.

Commit: `config: MCP configured — [list servers, or "none selected"]`

---

## Step 7 — Wire all links

Run from the repo root (use the venv Python so dependencies are available):

**macOS/Linux:**
```
.agent/.venv/bin/python .agent/tools/cli.py sync-links
```

**Windows:**
```
.agent\.venv\Scripts\python.exe .agent\tools\cli.py sync-links
```

This reads `.agent/config/shared_agent_config_symlinks.yaml` and creates:
- `.claude/commands → .agent/commands` (slash commands)
- `.mcp.json → .agent/mcp/config.json` (MCP server config)

On Windows without Developer Mode the tool automatically falls back to copying instead of symlinking and will tell you. That is expected — it still works.

Commit: `config: links wired`

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

**macOS/Linux:**
```
.agent/.venv/bin/python .agent/tools/cli.py --help
```
**Windows:**
```
.agent\.venv\Scripts\python.exe .agent\tools\cli.py --help
```

If it prints the command list without errors, the CLI is working. Then run a dry-run to confirm all links are in place:
```
.agent/.venv/bin/python .agent/tools/cli.py sync-links --dry-run
```
Every entry should show `skip` (already linked) or `warn` (target doesn't exist yet — acceptable for optional integrations). Any `would` line means a link still needs to be created; re-run without `--dry-run` to fix it.

List any incomplete items here as pending so the user is aware.

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
