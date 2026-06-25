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
@click.option("--dry-run", is_flag=True, default=False, help="Show what would be done without making changes.")
@click.option(
    "--config",
    default=None,
    type=click.Path(exists=False),
    help="Path to symlinks YAML (default: .agent/config/shared_agent_config_symlinks.yaml)",
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
    click.echo("Return to SETUP.md for the remaining steps (secrets, MCP servers, memory).")


if __name__ == "__main__":
    cli()
