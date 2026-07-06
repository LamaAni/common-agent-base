# [AGENT_NAME] — Your Personal AI Assistant

> **BETA** — actively developed. Works today; expect occasional rough edges.

A personal AI assistant that lives in your computer, knows your job and team, and handles tasks in plain English. No coding. No subscriptions beyond an LLM (Claude, Chat, Gemini, your company LLM).

You give it a task — it writes, researches, summarises, drafts, analyses — and saves everything in a **Work/** folder, organised by project.

---

## What you get

- A named assistant (you choose the name) that knows your role, company, and preferences
- All outputs filed automatically in **Work/**, one folder per project
- Slash commands for common tasks (`/summarize`, `/order`)
- Optional live connections to Slack, Google Drive, and more via MCP
- Local storage and version via git. 
- Remote storage via git (ask the agent).

---

## Setup — about 15 minutes, three steps

### 1. Install VS Code
Free download: [code.visualstudio.com](https://code.visualstudio.com) — click **Download** and run the installer.

### 2. Install your AI

Choose one and follow the link for full instructions:

| AI | Constitution | Commands | MCP |
|----|:---:|:---:|:---:|
| [Claude Code](.agent/docs/install-claude-code.md) | ✅ | ✅ | ✅ |
| [GitHub Copilot](.agent/docs/install-copilot.md) | ✅ | ❌ | ✅ |
| [Gemini Code Assist](.agent/docs/install-gemini.md) | ❌ | ❌ | ✅ |
| [ChatGPT / OpenAI](.agent/docs/install-chatgpt.md) | ❌ | ❌ | ✅ |

_Constitution = your assistant remembers your preferences across sessions. Commands = slash commands like `/summarize`. MCP = live connections to Slack, Google Drive, browser, etc._

### 3. Start setup

Open your AI chat and paste this [message](SETUP.md):

> Please follow the setup instructions at this URL and set up my workspace:
> `https://raw.githubusercontent.com/LamaAni/common-agent-base/main/SETUP.md?nocache=1`

> **Windows users:** if your AI fetches the URL but seems to be reading old instructions, add a random number to the end, e.g. `?nocache=42`. This forces a fresh fetch and bypasses any local cache.

Your assistant will download this repo, ask you a few questions about your name and team, and configure everything. Takes about 10 minutes.

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

Just ask your assistant. Examples:

- _"Connect me to Slack so you can read my channels"_
- _"Set up Google Drive so you can access my files"_
- _"Add a browser so you can research the web for me"_

Your assistant handles the configuration — you don't need to touch any files.

