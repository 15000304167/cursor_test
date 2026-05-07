from __future__ import annotations

import pytest

from dimos_testkit.adapters.mcp_cli import McpCliAdapter
from dimos_testkit.cli_wrappers.dimos_cmd import which_dimos
from dimos_testkit.paths import repo_root
from dimos_testkit.skills.registry import ToolRegistry


@pytest.mark.contract
@pytest.mark.mcp
def test_mcp_tools_cover_golden(case_artifacts) -> None:
    if not which_dimos():
        pytest.skip("dimos CLI not available")
    mcp = McpCliAdapter()
    names = mcp.list_tool_names()
    golden = repo_root() / "fixtures" / "tools_golden.json"
    diff = ToolRegistry(golden).diff(names)
    case_artifacts.append_meta({"runtime_tool_count": len(names), "golden": str(golden)})
    case_artifacts.write_json("runtime_tools.json", sorted(names))
    assert not diff.missing_in_runtime, (
        f"Golden tools missing at runtime: {sorted(diff.missing_in_runtime)} "
        f"(extras allowed: {sorted(diff.extra_in_runtime)})"
    )
