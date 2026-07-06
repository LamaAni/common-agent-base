# SETUP.md — Workspace Setup Instructions
_Read by an LLM agent from a URL. The repo is not yet on the user's machine when this runs._
_Non-interactive mode: if running without a user present, use dummy values where noted._
_If you fetched this file and it looks stale or truncated, re-fetch with a cache-busting param: append `?nocache=[random number]` to the URL._

---

## Before you start

Tell the user:
> "I'm going to set up your personal AI assistant. I'll start with a few quick questions, then handle the technical side automatically. This takes about 10 minutes."

Detect the user's operating system by running `uname -s` (Linux/macOS) or checking `%OS%` (Windows). Use this throughout to give OS-appropriate instructions.

---

## Step 1 — Interview

Ask every question below, one at a time, waiting for the answer before moving on.
Record all answers — you will use them to personalise the assistant and configure the workspace.

For any personal question the user can say **"skip"** — leave that placeholder blank and move on.

### A — Identity

1. "What should I call myself? This will be my name when I introduce myself to you. (e.g. Aria, Max, Sage)"

   Record as `[AGENT_NAME]`. After the user answers, say: "Great — I'll be [AGENT_NAME]."

2. "What's your name? (or say skip)"
3. "What company do you work at? (or say skip)"
4. "What's your team or department? (or say skip)"
5. "What's your role or title? (or say skip)"

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

8. "Which of these do you use at work? Pick all that apply:
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

### D — MCP integrations

9. "I can connect directly to your tools so I can read and act on your behalf. Which of these would you like?
   - Slack (read channels, send messages)
   - Google Drive (read and write files)
   - Browser (research websites for you)

   Pick any, all, or say 'none' to skip for now. These can be added anytime later."

Note which servers to configure. You will set them up in Step 8.

---

## Step 2 — Install location

Ask the user:

> "Where should I set up your workspace? Here are three options:
> 1. **This folder** — use wherever VS Code is open right now (`[CURRENT_DIR]`)
> 2. **Home folder** — create `~/[agent-name-lowercase]` in your home directory _(recommended)_
> 3. **Custom path** — tell me exactly where
>
> Just say 1, 2, or type a path."

Default to option 2 if the user presses Enter or says nothing. Expand `~` to the full home path. Record the chosen path as `[INSTALL_DIR]`.

---

## Step 3 — Bootstrap

### 3a — git

Check: `git --version`.

**If git is found:** confirm silently and move on.

**If git is missing:** install it directly:

- **Windows:** Run `winget install --silent Git.Git`. If winget is not available, tell the user to download from [git-scm.com/download/win](https://git-scm.com/download/win) and click Next on every screen. After either method, tell the user: "Git is installed — please restart VS Code so the terminal picks up the change, then come back." Wait for confirmation before continuing.
- **Mac:** Run `xcode-select --install`. This opens a system dialog the user must click through. Tell the user: "A dialog has appeared — click Install and come back when it finishes." Wait for confirmation.
- **Linux:** Run `sudo apt install -y git` (Ubuntu/Debian) or `sudo dnf install -y git` (Fedora).

Re-check `git --version`. Do not proceed until git works.

### 3b — Clone the repo

Run:
```
git clone https://github.com/LamaAni/common-agent-base.git [INSTALL_DIR]
```

Then change into the directory and confirm `AGENT.md` exists. If the clone fails (network error, directory already exists, etc.), tell the user in plain English and wait for them to resolve it before continuing.

Tell the user: "Great — I've downloaded your assistant workspace. Let's keep going."

---

## Step 4 — Prerequisites

### 4a — Python

Check: `python3 --version` (or `python --version` on Windows).

**If Python 3.10 or higher is found:** confirm silently and move on.

**If Python is missing or older than 3.10:** install it directly:

- **Windows:** Run `winget install --silent Python.Python.3.12`. After it completes, tell the user: "Python is installed — please restart VS Code so the terminal picks up the change, then come back." Wait for confirmation before continuing.
- **Mac:** Check if Homebrew is available by running `brew --version`. If yes, run `brew install python3`. If no, tell the user to download the installer from [python.org/downloads](https://python.org/downloads), open it, and follow the steps — then come back when done.
- **Linux:** Run `sudo apt install -y python3` (Ubuntu/Debian) or `sudo dnf install -y python3` (Fedora).

Re-check `python3 --version` (or `python --version` on Windows). Do not proceed until Python 3.10+ is confirmed.

---

## Step 5 — Personalise AGENT.md

`AGENT.md` is the agent constitution. Fill the placeholders directly in `AGENT.md` using the interview answers:

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

## Step 6 — Secrets setup

Copy `.env.example` to `.env`.

For each key in `.env.example`, ask the user in plain English what the value is and where to find it. Fill in any they provide. Leave blank any they do not have yet — they can add them later.

Tell the user: "You can add more keys to `.env` any time as you connect new services."

---

## Step 7 — Install

Run from the repo root:

**macOS/Linux:**
```
bash .agent/tools/install.sh
```
**Windows:**
```
.agent\tools\install.bat
```

This creates the Python venv, installs dependencies, then runs the CLI to wire all links and create the MCP config stub. Safe to re-run at any time.

Commit: `install: environment ready`

---

## Step 8 — MCP configuration

Read `.agent/mcp/servers.md` — it has the full config format, blocks for common servers, and rules for custom scripts.

Based on the user's answers in Step 1D, edit `.agent/mcp/config.json` (created by the install step as an empty stub):
- Add a block for each integration the user selected
- Leave `mcpServers: {}` if they selected none
- Put any required API keys in `.env` and reference them as `${KEY}` in the config — never hardcode secrets

If none selected: skip editing and note it as pending.

Commit: `config: MCP configured — [list servers, or "none selected"]`

---

## Step 9 — Memory bootstrap

Use the platform's memory tools to write the following. Do not hardcode a path — the platform manages memory automatically. Use the values already filled in `AGENT.md`.

**Memory index entry:**
```
- [User Profile](user_profile.md) — [USERNAME]'s role, context, and preferences
```

**`user_profile.md`:**
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

(Replace each `[...]` with the actual filled values from AGENT.md.)

---

## Step 10 — Verification

**macOS/Linux:**
```
.agent/.venv/bin/python .agent/tools/cli.py sync-links --dry-run
```
**Windows:**
```
.agent\.venv\Scripts\python.exe .agent\tools\cli.py sync-links --dry-run
```

Every entry should show `skip` (already linked) or `warn` (target missing — acceptable for optional integrations not yet configured). Any `would` means a link still needs creating; re-run `install.sh` to fix it.

---

## Step 11 — Open VS Code and restart

Run `code [INSTALL_DIR]` to open the workspace in VS Code. If `code` is not found in PATH, tell the user:
> "Please open VS Code, go to **File → Open Folder**, and select `[INSTALL_DIR]`."

Build the summary dynamically from what actually happened in steps 1–11. Then tell the user:

> "Setup is complete — VS Code is opening your workspace now. **Please close this conversation and open a new one inside VS Code.** In the new session I'll introduce myself as [AGENT_NAME] and I'll already know your context.
>
> **What's ready now:** [list completed steps in plain English]
>
> **Coming in future updates:** [list skipped steps with plain-English reason]
>
> You can already ask me to write documents, summaries, analyses, draft emails, or any other task — I'll organise everything in your **Work/** folder by project."
