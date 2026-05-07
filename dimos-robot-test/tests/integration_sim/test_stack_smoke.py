from __future__ import annotations

import pytest

from dimos_testkit.assertions.health import assert_dimos_status_ok
from dimos_testkit.cli_wrappers.dimos_cmd import run_dimos


@pytest.mark.integration
@pytest.mark.sim
def test_dimos_status_after_stack(dimos_stack) -> None:
    assert_dimos_status_ok(run_dimos(["status"], timeout=30.0))
