from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from dimos_testkit.reporting.junit import attach_ci_properties


def _terminal_counts(session: pytest.Session) -> dict[str, int]:
    pm = session.config.pluginmanager
    term = pm.get_plugin("terminalreporter") if hasattr(pm, "get_plugin") else pm.getplugin("terminalreporter")
    if not term or not getattr(term, "stats", None):
        return {}
    out: dict[str, int] = {}
    for k, reps in term.stats.items():
        out[k] = len(reps)
    return out


def write_session_summary(path: Path, session: pytest.Session, exitstatus: int) -> None:
    """Write ``summary.json`` for dashboards and artifact correlation."""
    counts = _terminal_counts(session)
    payload: dict[str, Any] = {
        "exitstatus": exitstatus,
        "testscollected": getattr(session, "testscollected", None),
        "counts": counts,
        "properties": attach_ci_properties(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
