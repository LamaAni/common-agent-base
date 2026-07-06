from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


# ---------------------------------------------------------------------------
# Repo root helper
# ---------------------------------------------------------------------------

def _repo_root() -> Path:
    """Walk up from this file until we find the directory containing .agent/."""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".agent").is_dir():
            return parent
    raise RuntimeError("Could not locate repo root (no .agent/ directory found).")


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

class JSONIndexEntryType(StrEnum):
    General = "general"
    Command = "command"
    DataSource = "datasource"
    Procedure = "procedure"
    Work = "work"
    Tool = "tool"
    Doc = "doc"


@dataclass
class JSONIndexEntry:
    type: JSONIndexEntryType
    description: str        # what the file contains (one sentence)
    use: str                # when to load this file
    keywords: list[str]     # searchable tags
    added_on: int = field(default_factory=lambda: int(time.time()))

    def to_dict(self) -> dict:
        return {
            "type": str(self.type),
            "description": self.description,
            "use": self.use,
            "keywords": self.keywords,
            "added_on": self.added_on,
        }

    @staticmethod
    def from_dict(d: dict) -> "JSONIndexEntry":
        return JSONIndexEntry(
            type=JSONIndexEntryType(d["type"]),
            description=d["description"],
            use=d["use"],
            keywords=d.get("keywords", []),
            added_on=d.get("added_on", 0),
        )


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

class JSONIndex:
    WARN_TOKENS = 10_000
    _CHARS_PER_TOKEN = 4

    def __init__(self, storage_path: str | Path) -> None:
        self.storage_path = Path(storage_path)
        self.index: dict[str, JSONIndexEntry] = {}

    # --- persistence --------------------------------------------------------

    def load(self) -> None:
        """Load entries from disk. Safe to call even if the file doesn't exist yet."""
        if not self.storage_path.exists():
            self.index = {}
            return
        raw = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self.index = {
            name: JSONIndexEntry.from_dict(entry)
            for name, entry in raw.get("entries", {}).items()
        }

    def save(self) -> None:
        """Persist entries to disk as minified JSON (no extra whitespace)."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "_doc": "Workspace index. Keys in 'entries' are repo-relative file paths. Each value describes the file's purpose and when the LLM should load it.",
            "v": 1,
            "warn": self.WARN_TOKENS,
            "entries": {name: e.to_dict() for name, e in self.index.items()},
        }
        self.storage_path.write_text(
            json.dumps(payload, separators=(",", ":")),
            encoding="utf-8",
        )

    # --- mutation -----------------------------------------------------------

    def add(self, name: str, entry: JSONIndexEntry) -> str:
        """Add or overwrite an entry. Returns a status string."""
        verb = "updated" if name in self.index else "added"
        self.index[name] = entry
        self.save()
        tokens = self.token_estimate()
        suffix = (
            f"  !! ~{tokens} tokens — approaching {self.WARN_TOKENS} limit"
            if tokens >= self.WARN_TOKENS else ""
        )
        return f"{verb}: {name}{suffix}"

    def remove(self, name: str) -> str:
        """Remove an entry by name. Returns a status string."""
        if name not in self.index:
            return f"not found: {name}"
        del self.index[name]
        self.save()
        return f"removed: {name}"

    # --- queries ------------------------------------------------------------

    def list(self, since: int = -1) -> list[tuple[str, JSONIndexEntry]]:
        """Return (name, entry) pairs, optionally filtered to added_on > since."""
        items = self.index.items()
        if since >= 0:
            items = ((n, e) for n, e in items if e.added_on > since)
        return list(items)

    def search(self, pattern: str) -> list[tuple[str, JSONIndexEntry]]:
        """Return entries whose name, description, use, or keywords match the regex."""
        rx = re.compile(pattern, re.IGNORECASE)
        return [
            (name, entry)
            for name, entry in self.index.items()
            if rx.search(name)
            or rx.search(entry.description)
            or rx.search(entry.use)
            or any(rx.search(k) for k in entry.keywords)
        ]

    # --- diagnostics --------------------------------------------------------

    def token_estimate(self) -> int:
        """Rough token count estimate based on serialised size."""
        return len(self.storage_path.read_bytes()) // self._CHARS_PER_TOKEN if self.storage_path.exists() else 0

    def format_entry(self, name: str, entry: JSONIndexEntry) -> str:
        """Single compact line for LLM context."""
        kw = ",".join(entry.keywords)
        return f"[{entry.type:<9}] {name} | {entry.description} | {entry.use} | kw:{kw}"

    # --- factory ------------------------------------------------------------

    @classmethod
    def default(cls) -> "JSONIndex":
        """Return an index pointed at the default .agent/index.json location."""
        return cls(_repo_root() / ".agent" / "index.json")
