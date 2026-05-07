from __future__ import annotations

import json

import pytest

from dimos_testkit.adapters.mcp_cli import McpCliAdapter


@pytest.mark.integration
@pytest.mark.mcp
def test_mcp_transcript_written(dimos_stack, case_artifacts) -> None:
    mcp = McpCliAdapter()
    st = mcp.status_raw()
    lt = mcp.list_tools_raw()
    transcript = [
        {"step": "status", "returncode": st.returncode, "stdout": st.stdout[:4000]},
        {"step": "list-tools", "returncode": lt.returncode, "stdout": lt.stdout[:4000]},
    ]
    path = case_artifacts.write_text("mcp_transcript.jsonl", json.dumps(transcript, indent=2))
    assert path.exists()
