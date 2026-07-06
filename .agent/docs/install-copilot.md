# Installing GitHub Copilot

GitHub Copilot works with this repo for chat and task assistance. Slash commands and MCP are not supported — your assistant will still organise Work/ and follow your preferences, but via chat rather than commands.

## 1. Get a Copilot subscription
Copilot requires a GitHub account with a paid Copilot plan.
- Individual: [github.com/features/copilot](https://github.com/features/copilot) — sign up and choose a plan
- Business/Enterprise: ask your IT or GitHub admin — you may already have access

## 2. Install the VS Code extension
Inside VS Code, press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac).
Search **GitHub Copilot Chat**, click **Install**. (Install both **GitHub Copilot** and **GitHub Copilot Chat**.)

## 3. Sign in
Click the Copilot icon in the sidebar and sign in with your GitHub account.

## 4. Point Copilot at AGENT.md
Copilot reads instructions from `.github/copilot-instructions.md`, not `CLAUDE.md`.
After setup fills in your preferences in `AGENT.md`, copy it:
```
cp AGENT.md .github/copilot-instructions.md
```
Create `.github/` if it doesn't exist.

## 5. Return to setup
Go back to the README and continue with step 3 (get this repo).

---

| Feature | Support |
|---------|---------|
| Constitution | ✅ Via `.github/copilot-instructions.md` (step 4 above) |
| Slash commands | ❌ |
| MCP integrations | ✅ |
