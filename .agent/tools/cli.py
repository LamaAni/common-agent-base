"""
cli.py — entry point for the common-agent-base toolchain.

Usage:
    python .agent/tools/cli.py --help
    python .agent/tools/cli.py setup
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
    """Create symlinks defined in shared_agent_config_symlinks.yaml."""
    from sync_links.sync_links import sync  # type: ignore

    config_path = Path(config) if config else None
    results = sync(config_path=config_path, dry_run=dry_run)
    for line in results:
        click.echo(line)


@cli.command("setup")
def setup() -> None:
    """Run full agent setup: create links, verify environment."""
    click.echo("=== common-agent-base setup ===\n")

    # Step 1: sync links
    click.echo("Wiring links...")
    from sync_links.sync_links import sync  # type: ignore

    results = sync()
    for line in results:
        click.echo(line)

    click.echo("\nSetup complete.")
    click.echo("Next: follow remaining steps in SETUP.md (secrets, MCP, memory).")


if __name__ == "__main__":
    cli()
