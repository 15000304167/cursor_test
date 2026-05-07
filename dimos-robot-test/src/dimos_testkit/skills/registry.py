from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ToolDiff:
    missing_in_runtime: frozenset[str]
    extra_in_runtime: frozenset[str]

    @property
    def ok(self) -> bool:
        return not self.missing_in_runtime and not self.extra_in_runtime


class ToolRegistry:
    """Compare golden tool names with runtime MCP ``list-tools`` output."""

    def __init__(self, golden_path: Path) -> None:
        self._golden_path = golden_path

    def golden_names(self) -> set[str]:
        raw = json.loads(self._golden_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and "tools" in raw:
            tools = raw["tools"]
        elif isinstance(raw, list):
            tools = raw
        else:
            raise ValueError("golden file must be a list of names or {\"tools\": [...]}")
        names: set[str] = set()
        for item in tools:
            if isinstance(item, str):
                names.add(item)
            elif isinstance(item, dict) and "name" in item:
                names.add(str(item["name"]))
        return names

    def diff(self, runtime_names: Iterable[str]) -> ToolDiff:
        golden = self.golden_names()
        runtime = set(runtime_names)
        return ToolDiff(
            missing_in_runtime=frozenset(sorted(golden - runtime)),
            extra_in_runtime=frozenset(sorted(runtime - golden)),
        )
