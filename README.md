# [AGENT_NAME] — Your Personal AI Assistant

> **BETA** — actively developed. Works today; expect occasional rough edges.

A personal AI assistant that lives in your computer, knows your job and team, and handles tasks in plain English. No coding. No subscriptions beyond Claude.

You give it a task — it writes, researches, summarises, drafts, analyses — and saves everything in a **Work/** folder, organised by project.

---

## What you get

- A named assistant (you choose the name) that knows your role, company, and preferences
- All outputs filed automatically in **Work/**, one folder per project
- Slash commands for common tasks (`/summarize`, `/order`) — see `.agent/commands/index.md`
- Optional live connections to Slack, Google Drive, and more via MCP

---

## Setup — about 15 minutes, four steps

### 1. Install VS Code
Free download: [code.visualstudio.com](https://code.visualstudio.com) — click **Download** and run the installer.

### 2. Install Claude Code
Inside VS Code, press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac).
Search **Claude Code**, click **Install**.

You'll need an Anthropic account — sign up free at [claude.ai](https://claude.ai).

### 3. Get this repo

**No git? Download the ZIP:**
1. Click the green **Code** button at the top of this page
2. Click **Download ZIP**
3. Unzip the folder somewhere easy to find (e.g. `Documents/my-assistant`)

**Have git?**
```
git clone https://github.com/LamaAni/common-agent-base.git my-assistant
```

### 4. Open and run setup
1. In VS Code: **File → Open Folder** → select the folder you just unzipped or cloned
2. Claude Code will open in the sidebar (look for the Claude icon)
3. Type exactly:

   > _Please follow SETUP.md and set up my workspace._

Claude will ask your name, your team, what to call your assistant, and a few preferences. It handles the rest — takes about 10 minutes.

---

## After setup

Drop tasks in plain English. Examples:

- _"Summarise this report and pull out the key risks"_
- _"Draft an email to the leadership team about the Q3 results"_
- _"Research our top three competitors and compare their pricing"_
- _"What are the action items from this meeting transcript?"_

Results go into **Work/**, organised by project.

---

## Adding integrations later

To connect Slack, Google Drive, or a browser, edit `.agent/mcp/config.json` — see `.agent/mcp/servers.md` for the format and available servers.

