---
name: summarize
description: Summarise a document, URL, or pasted text and save the result to Work/
---

1. Ask the user:
   > "What would you like me to summarise? You can:
   > - Paste the text directly here
   > - Share a URL and I'll read it
   > - Give me the file name if you've already shared a file"

2. Read the content in full before writing anything.

3. Write a plain-English summary using this structure:
   - **One-line TL;DR** — the single most important thing to know
   - **Key points** — 3–7 bullets, each one a complete thought
   - **Actions or decisions** — only if any are present in the source; skip this section if not

   Rules: no jargon, no "this document discusses...", no filler. Write as if explaining to a busy executive who has 30 seconds.

4. Follow order rules (see `.agent/commands/order.md`):
   - Run `cli.py index search [topic]` to find an existing project this belongs to
   - If unsure, ask: "Should I file this under an existing project, or create a new one?"
   - Save to `Work/[project]/summary_YYYYMMDD.md`
   - Run `cli.py index add --path Work/[project]/summary_YYYYMMDD.md --type work --about "[topic] summary" --use "[keywords]"`

5. Commit:
   ```
   output: summary of [source name or topic]
   ```

6. Tell the user:
   > "Done — your summary is in Work/[project]/. Here's the TL;DR:
   > [paste the one-liner]"
