---
name: order
description: Organisation rules for Work/. Always active — follow these before creating any output.
---

# Order Rules

These rules apply every time the agent creates a file in `Work/`. They are not optional. The user should never need to clean up or re-sort outputs.

---

## Before creating any file

1. Read `Work/INDEX.md` to see what projects already exist.
2. Decide: does this output belong to an existing project, or is it new?
3. If unsure, ask the user: "Is this part of an existing project, or something new? Here's what I have so far: [list current projects]"

---

## Project folder rules

- One folder per topic or project: `Work/[topic-slug]/`
- Slug format: lowercase, hyphens, no spaces
  - Good: `vendor-negotiation/`, `q3-planning/`, `hiring-process/`
  - Bad: `Vendor Negotiation/`, `Q3_Planning/`, `misc/`
- Reuse existing project folders where they fit — don't create near-duplicates
- Create `Work/[project]/INDEX.md` immediately when creating a new project folder

---

## File naming

```
[short-description]_YYYYMMDD.[ext]
```

Examples:
- `competitor-analysis_20260624.md`
- `board-update-draft_20260618.md`
- `q2-sales-data_20260601.csv`

No spaces. No generic names like `summary.md` or `output.md`.

---

## INDEX.md updates — mandatory, every time

After creating any file:

1. Add a row to `Work/[project]/INDEX.md`:
```
| filename | YYYY-MM-DD | One-line description of what's in this file |
```

2. If the project folder is new, add a row to `Work/INDEX.md`:
```
| [project-slug](project-slug/INDEX.md) | YYYY-MM-DD | One-line description of this project |
```

Never create a file without updating both relevant indexes immediately after. No exceptions.

---

## Commits

After any file creation + index update, commit:
```
output: [plain-English description of what was created]
project: [slug] created   ← only if a new project folder was created
index: Work/[project] updated
```

---

## If the user invokes /order

Show a summary of the current Work/ state:
```
Here's what I have organised in Work/:

[project-slug] — [description] — [N] file(s) — last updated [date]
...

Total: [N] projects, [N] files.
```

Then ask: "Would you like me to rename anything, move a file to a better project, or add any missing descriptions to the index?"
