from __future__ import annotations

import os
from typing import Any

import httpx

from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult


def default_mcp_url() -> str:
    base = os.environ.get("DIMOS_MCP_URL", "http://127.0.0.1:9990").rstrip("/")
    path = os.environ.get("DIMOS_MCP_PATH", "/mcp")
    if not path.startswith("/"):
        path = "/" + path
    return base + path


class McpHttpClient:
    """Optional JSON-RPC style client for MCP HTTP endpoint (falls back to CLI in tests)."""

    def __init__(self, endpoint: str | None = None, *, timeout_s: float = 30.0) -> None:
        self.endpoint = endpoint or default_mcp_url()
        self._timeout = timeout_s

    def _post_rpc(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(self.endpoint, json=body, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(str(data["error"]))
        if not isinstance(data, dict) or "result" not in data:
            raise RuntimeError(f"Unexpected MCP HTTP response: {data!r}")
        result = data["result"]
        if not isinstance(result, dict):
            raise RuntimeError(f"Unexpected result type: {type(result)}")
        return result

    def tools_list(self) -> dict[str, Any]:
        """Call ``tools/list``; raises if transport or method unsupported."""
        return self._post_rpc("tools/list")

    def tools_call(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """Call ``tools/call`` with DimOS-style arguments."""
        params = {"name": name, "arguments": arguments or {}}
        return self._post_rpc("tools/call", params)


def tools_list_to_dimos_result(client: McpHttpClient) -> DimosCmdResult:
    try:
        result = client.tools_list()
        return DimosCmdResult(stdout=str(result), stderr="", returncode=0)
    except Exception as e:  # noqa: BLE001 — surface as failed command
        return DimosCmdResult(stdout="", stderr=str(e), returncode=1)
