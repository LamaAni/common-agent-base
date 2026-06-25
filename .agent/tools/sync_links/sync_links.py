"""
sync_links.py — create symlinks defined in shared_agent_config_symlinks.yaml.

All paths in the YAML are repo-root-relative.
For each link:
  1. Resolve both paths from the repo root.
  2. Compute the symlink target as relative from the link's parent directory.
  3. Try os.symlink(); on PermissionError (Windows without Developer Mode),
     fall back to shutil copy.

Idempotent: skips links that already exist and are correct.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _repo_root() -> Path:
    """Walk up from this file to find the repo root (contains .agent/)."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".agent").is_dir():
            return parent
    raise RuntimeError("Cannot locate repo root (no .agent/ directory found in parents)")


def _load_config(config_path: Path) -> list[dict]:
    try:
        import yaml  # type: ignore
    except ImportError:
        print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
        sys.exit(1)
    with config_path.open() as f:
        data = yaml.safe_load(f)
    return data.get("links", [])


def _is_valid_link(link_path: Path, expected_target: Path) -> bool:
    """Return True if link_path is already a symlink pointing at expected_target."""
    if link_path.is_symlink():
        actual = (link_path.parent / os.readlink(link_path)).resolve()
        return actual == expected_target.resolve()
    return False


def _copy_fallback(target: Path, link_path: Path) -> None:
    """Copy target into link_path location (Windows fallback)."""
    if link_path.exists():
        if link_path.is_dir():
            shutil.rmtree(link_path)
        else:
            link_path.unlink()
    if target.is_dir():
        shutil.copytree(target, link_path)
    else:
        link_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, link_path)


def sync(config_path: Path | None = None, *, dry_run: bool = False) -> list[str]:
    """
    Create all symlinks defined in the config.
    Returns a list of human-readable result lines.
    """
    root = _repo_root()
    if config_path is None:
        config_path = root / ".agent" / "setup" / "shared_agent_config_symlinks.yaml"

    if not config_path.exists():
        return [f"ERROR: config not found: {config_path}"]

    links = _load_config(config_path)
    results = []

    for entry in links:
        from_rel = entry["from"]
        to_rel = entry["to"]

        link_path = root / from_rel          # absolute path of the link to create
        target_abs = root / to_rel           # absolute path of what it points at

        # Compute the symlink target relative to the link's parent directory.
        # e.g. .claude/commands -> .agent/commands becomes ../agent/commands
        symlink_target = Path(os.path.relpath(target_abs, link_path.parent))

        label = f"{from_rel} -> {to_rel}"

        # Already correct
        if _is_valid_link(link_path, target_abs):
            results.append(f"  skip    {label}  (already correct)")
            continue

        # Target must exist (unless it's a .gitkeep-only dir we still want to wire)
        if not target_abs.exists():
            results.append(f"  warn    {label}  (target does not exist yet, skipping)")
            continue

        if dry_run:
            results.append(f"  would   {label}")
            continue

        # Remove stale link or broken text file
        if link_path.exists() or link_path.is_symlink():
            if link_path.is_dir() and not link_path.is_symlink():
                shutil.rmtree(link_path)
            else:
                link_path.unlink()

        link_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            target_is_dir = target_abs.is_dir()
            os.symlink(symlink_target, link_path, target_is_directory=target_is_dir)
            results.append(f"  linked  {label}")
        except PermissionError:
            # Windows without Developer Mode — fall back to copy
            _copy_fallback(target_abs, link_path)
            results.append(
                f"  copied  {label}"
                f"  (symlink needs Developer Mode on Windows; used copy fallback)"
            )

    return results
