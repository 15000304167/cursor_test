from __future__ import annotations

import os
from pathlib import Path


def dimos_state_dir() -> Path:
    """Default DimOS state directory (override with DIMOS_STATE_DIR for tests)."""
    override = os.environ.get("DIMOS_STATE_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".local" / "state" / "dimos"
