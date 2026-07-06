"""
cli.py — entry point for the common-agent-base toolchain.

Usage:
    python .agent/tools/cli.py --help
    python .agent/tools/cli.py install
    python .agent/tools/cli.py sync-links [--dry-run]
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal dependency check before importing click
# ---------------------------------------------------------------------------
try:
    import click
except ImportError:
    print(
        "ERROR: 'click' not installed.\n"
        "Run: pip install click   (or: python -m pip install click)",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Resolve repo root so sub-tools can import from .agent/tools/
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / ".agent" / "tools"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _step(label: str) -> None:
    click.echo(f"\n-- {label}")


def _ok(msg: str) -> None:
    click.echo(f"   ok  {msg}")


def _skip(msg: str) -> None:
    click.echo(f" skip  {msg}")


def _warn(msg: str) -> None:
    click.echo(f" warn  {msg}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@click.group()
def cli() -> None:
    """common-agent-base toolchain."""


@cli.command("sync-links")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Show what would be done without making changes.",
)
@click.option(
    "--config",
    default=None,
    type=click.Path(exists=False),
    help="Path to symlinks YAML (default: .agent/setup/shared_agent_config_symlinks.yaml)",
)
def sync_links(dry_run: bool, config: str | None) -> None:
    """Create or refresh symlinks defined in shared_agent_config_symlinks.yaml."""
    from sync_links.sync_links import sync  # type: ignore

    config_path = Path(config) if config else None
    results = sync(config_path=config_path, dry_run=dry_run)
    for line in results:
        click.echo(line)


@cli.command("install")
def install() -> None:
    """Wire links and create MCP stub. Run via install.sh / install.bat on first use."""
    click.echo("=== common-agent-base install ===")

    # 1 — MCP config stub
    _step("MCP config stub")
    mcp_config = _REPO_ROOT / ".agent" / "mcp" / "config.json"
    if mcp_config.exists():
        _skip(".agent/mcp/config.json already exists")
    else:
        mcp_config.parent.mkdir(parents=True, exist_ok=True)
        mcp_config.write_text('{\n  "mcpServers": {}\n}\n', encoding="utf-8")
        _ok("created .agent/mcp/config.json (empty stub)")

    # 2 — Symlinks / copy fallback
    _step("Links")
    from sync_links.sync_links import sync  # type: ignore

    for line in sync():
        click.echo(f"  {line.strip()}")

    click.echo("\nInstall complete.")
    click.echo(
        "Return to SETUP.md for the remaining steps (secrets, MCP servers, memory)."
    )


@cli.group()
def index() -> None:
    """Manage the workspace index (.agent/index.json)."""


def _load_index():
    from index_manager.index_manager import JSONIndex  # type: ignore

    idx = JSONIndex.default()
    idx.load()
    return idx


@index.command("add")
@click.option(
    "--path", required=True, help="Repo-relative file path (used as the entry key)."
)
@click.option(
    "--type",
    "type_",
    required=True,
    type=click.Choice(
        ["work", "command", "tool", "doc", "general", "datasource", "procedure"]
    ),
    help="Entry type.",
)
@click.option("--about", required=True, help="One sentence: what the file contains.")
@click.option("--use", required=True, help="When to load this file (plain English).")
@click.option("--keywords", default="", help="Comma-separated search tags (optional).")
def index_add(path: str, type_: str, about: str, use: str, keywords: str) -> None:
    """Add or update an entry in the workspace index."""
    from index_manager.index_manager import JSONIndexEntry, JSONIndexEntryType  # type: ignore

    idx = _load_index()
    entry = JSONIndexEntry(
        type=JSONIndexEntryType(type_),
        description=about,
        use=use,
        keywords=[k.strip() for k in keywords.split(",") if k.strip()],
    )
    click.echo(idx.add(path, entry))


@index.command("remove")
@click.option("--path", required=True, help="Repo-relative file path to remove.")
def index_remove(path: str) -> None:
    """Remove an entry from the workspace index."""
    idx = _load_index()
    click.echo(idx.remove(path))


@index.command("search")
@click.argument("pattern")
def index_search(pattern: str) -> None:
    """Search the index with a regex (matches path, description, use, keywords)."""
    idx = _load_index()
    results = idx.search(pattern)
    if not results:
        click.echo("no matches")
        return
    for name, entry in results:
        click.echo(idx.format_entry(name, entry))
    click.echo(f"--- {len(results)} match(es)")


@index.command("print")
@click.option("--type", "type_", default=None, help="Filter by entry type.")
def index_print(type_: str | None) -> None:
    """Print the index in compact format (for loading into LLM context)."""
    idx = _load_index()
    items = idx.list()
    if type_:
        items = [(n, e) for n, e in items if str(e.type) == type_]
    for name, entry in items:
        click.echo(idx.format_entry(name, entry))
    tokens = idx.token_estimate()
    click.echo(
        f"--- entries:{len(idx.index)}  tokens~:{tokens}  limit:{idx.WARN_TOKENS}"
    )
    if tokens >= idx.WARN_TOKENS:
        click.echo(
            "!! WARNING: index approaching token limit — archive old work entries"
        )


@index.command("delta")
@click.option(
    "--since",
    required=True,
    help="Unix timestamp or ISO 8601 UTC — show only entries added after this time.",
)
def index_delta(since: str) -> None:
    """Show entries added since a given time (use mid-session to avoid full reload)."""
    idx = _load_index()
    # Accept either unix int or ISO string
    try:
        since_ts = int(since)
    except ValueError:
        from datetime import datetime, timezone

        since_ts = int(
            datetime.fromisoformat(since.rstrip("Z"))
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
    items = idx.list(since=since_ts)
    if not items:
        click.echo(f"no new entries since {since}")
        return
    for name, entry in items:
        click.echo(idx.format_entry(name, entry))
    click.echo(f"--- {len(items)} new entry/entries")


if __name__ == "__main__":
    cli()
