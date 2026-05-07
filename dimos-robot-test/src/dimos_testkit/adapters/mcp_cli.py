from __future__ import annotations

import json
import os
from typing import Any

from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult, run_dimos


def _extract_json_value(text: str) -> Any:
    text = text.strip()
    for start_ch in ("{", "["):
        idx = text.find(start_ch)
        if idx != -1:
            return json.loads(text[idx:])
    raise ValueError("No JSON object or array found in dimos mcp output")


class McpCliAdapter:
    """Invoke DimOS MCP tools via ``dimos mcp`` CLI."""

    def __init__(self, *, call_timeout_s: float | None = None) -> None:
        env_timeout = os.environ.get("DIMOS_MCP_CALL_TIMEOUT")
        self._call_timeout = float(env_timeout) if env_timeout else (call_timeout_s or 120.0)

    def list_tools_raw(self) -> DimosCmdResult:
        return run_dimos(["mcp", "list-tools"], timeout=120.0)

    def list_tools_payload(self) -> Any:
        r = self.list_tools_raw()
        if not r.ok:
            raise RuntimeError(f"list-tools failed ({r.returncode}): {r.stderr}\n{r.stdout}")
        return _extract_json_value(r.stdout)

    def list_tool_names(self) -> list[str]:
        payload = self.list_tools_payload()
        names: list[str] = []
        if isinstance(payload, dict) and "tools" in payload:
            for t in payload["tools"]:
                if isinstance(t, dict) and "name" in t:
                    names.append(str(t["name"]))
        elif isinstance(payload, list):
            for t in payload:
                if isinstance(t, dict) and "name" in t:
                    names.append(str(t["name"]))
                elif isinstance(t, str):
                    names.append(t)
        return sorted(set(names))

    def call_skill(self, name: str, args: dict[str, Any] | None = None) -> DimosCmdResult:
        cmd = ["mcp", "call", name]
        if args:
            cmd.extend(["--json-args", json.dumps(args)])
        return run_dimos(cmd, timeout=self._call_timeout)

    def status_raw(self) -> DimosCmdResult:
        return run_dimos(["mcp", "status"], timeout=60.0)
