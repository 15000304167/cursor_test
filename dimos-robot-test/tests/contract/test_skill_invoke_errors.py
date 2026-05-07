from __future__ import annotations

import pytest

from dimos_testkit.adapters.mcp_cli import McpCliAdapter
from dimos_testkit.cli_wrappers.dimos_cmd import which_dimos


@pytest.mark.contract
@pytest.mark.mcp
def test_unknown_skill_returns_nonzero() -> None:
    if not which_dimos():
        pytest.skip("dimos CLI not available")
    mcp = McpCliAdapter()
    r = mcp.call_skill("__nonexistent_skill__", {})
    assert r.returncode != 0 or "error" in (r.stdout + r.stderr).lower()
