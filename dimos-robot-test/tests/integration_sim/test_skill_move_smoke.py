from __future__ import annotations

import os

import pytest

from dimos_testkit.assertions.responses import assert_non_empty_text
from dimos_testkit.skills.contracts import MoveSkillArgs


@pytest.mark.integration
@pytest.mark.sim
@pytest.mark.mcp
@pytest.mark.slow
def test_move_skill_smoke(dimos_stack, case_artifacts) -> None:
    """Low-velocity move against replay/sim profile; skipped if ``move`` tool absent."""
    args = MoveSkillArgs(x=float(os.environ.get("TEST_MOVE_X", "0.05")), duration=0.5)
    r = dimos_stack.call_skill("move", args.model_dump())
    case_artifacts.write_text("move_call_stdout.txt", r.stdout)
    case_artifacts.write_text("move_call_stderr.txt", r.stderr)
    if r.returncode != 0 and "unknown" in (r.stderr + r.stdout).lower():
        pytest.skip("move skill not available in this blueprint")
    assert r.ok, f"move failed: {r.stderr}\n{r.stdout}"
    assert_non_empty_text(r.stdout, label="move stdout")
