from __future__ import annotations

import pytest

from dimos_testkit.adapters.mcp_http import McpHttpClient


@pytest.mark.contract
@pytest.mark.mcp
def test_mcp_http_tools_list_optional() -> None:
    """If DimOS MCP HTTP speaks JSON-RPC ``tools/list``, validate; otherwise skip."""
    client = McpHttpClient(timeout_s=5.0)
    try:
        result = client.tools_list()
    except Exception:  # noqa: BLE001
        pytest.skip("MCP HTTP not reachable or protocol differs; use CLI adapter in CI.")
    assert isinstance(result, dict)
