from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return dimos-robot-test repository root (parent of ``src``)."""
    return Path(__file__).resolve().parent.parent.parent


def configs_dir() -> Path:
    return repo_root() / "configs"
