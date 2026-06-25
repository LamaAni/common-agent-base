# MCP Server Reference

Claude Code reads `.mcp.json` at startup. That file is a symlink to `.agent/mcp/config.json`, created by `install.sh`.

## Config format

`.agent/mcp/config.json`:
```json
{
  "mcpServers": {
    "[name]": {
      "command": "[executable]",
      "args": ["[arg1]", "[arg2]"],
      "env": { "KEY": "${KEY}" }
    }
  }
}
```

`env` values prefixed with `${...}` are resolved from the shell environment — put secrets in `.env`, not in this file.

After editing `config.json`, re-run `install.sh` / `install.bat` to refresh the `.mcp.json` link.

---

## Common servers

**Browser / web research**
```json
"browser": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```
Requires: Node.js

**Slack**
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
}
```
Requires: Node.js, `SLACK_BOT_TOKEN` in `.env`

**Google Drive**
```json
"gdrive": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gdrive"]
}
```
Requires: Node.js

---

## Custom / local servers

All custom MCP server scripts must live under `.agent/`:
```
.agent/
  mcp/
    servers/
      my_tool/
        server.py    ← MCP server entrypoint
        README.md    ← what it does, env vars required
```

Register in `config.json`:
```json
"my_tool": {
  "command": ".agent/.venv/bin/python",
  "args": [".agent/mcp/servers/my_tool/server.py"],
  "env": { "MY_API_KEY": "${MY_API_KEY}" }
}
```

Add any new pip dependencies to `.agent/setup/requirements.txt` and re-run `install.sh`.
