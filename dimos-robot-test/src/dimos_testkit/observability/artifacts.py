from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _safe_nodeid(nodeid: str) -> str:
    return nodeid.replace("::", "__").replace("/", "_").replace(":", "_")


@dataclass
class CaseArtifacts:
    """Per-test artifact directory (logs, transcripts, dimos log dumps)."""

    root: Path
    nodeid: str
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.dir = (self.root / _safe_nodeid(self.nodeid)).resolve()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.append_meta(
            {
                "nodeid": self.nodeid,
                "TEST_PROFILE": os.environ.get("TEST_PROFILE"),
                "GIT_SHA": os.environ.get("GIT_SHA") or os.environ.get("GITHUB_SHA"),
            }
        )

    def append_meta(self, extra: dict[str, Any]) -> None:
        self.meta.update(extra)
        (self.dir / "meta.json").write_text(json.dumps(self.meta, indent=2), encoding="utf-8")

    def write_text(self, name: str, content: str) -> Path:
        p = self.dir / name
        p.write_text(content, encoding="utf-8")
        return p

    def write_json(self, name: str, obj: Any) -> Path:
        p = self.dir / name
        p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
        return p
