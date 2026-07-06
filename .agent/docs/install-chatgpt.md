# Installing ChatGPT / OpenAI in VS Code

OpenAI does not publish an official VS Code extension. The best ways to use ChatGPT (GPT-4o, o3) with VS Code and this repo are below.

## Option A — Continue (recommended, free extension)

[Continue](https://continue.dev) is an open-source VS Code extension that connects to any AI, including OpenAI models.

1. Inside VS Code, press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
2. Search **Continue**, click **Install**
3. On first run, choose **OpenAI** and paste your API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Select your model (e.g. `gpt-4o`)

Continue supports custom system prompts — paste the contents of `AGENT.md` as your system prompt in Continue's config.

## Option B — GitHub Copilot (uses GPT-4o)

GitHub Copilot now runs on GPT-4o by default. If you have a GitHub Copilot subscription you're already using OpenAI models — see [install-copilot.md](install-copilot.md).

## Option C — ChatGPT web + VS Code side-by-side

No extension needed. Keep [chat.openai.com](https://chat.openai.com) open in a browser next to VS Code. Paste tasks and file contents manually. Paste results back into your Work/ folder.

---

| Feature | Support |
|---------|---------|
| Constitution | ❌ |
| Slash commands | ❌ |
| MCP integrations | ✅ (Option A via Continue) |

> For the best experience with this repo, Claude Code (see [install-claude-code.md](install-claude-code.md)) is recommended.
