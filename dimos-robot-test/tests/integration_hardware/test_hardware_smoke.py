from __future__ import annotations

import pytest

from dimos_testkit.assertions.health import assert_dimos_status_ok
from dimos_testkit.cli_wrappers.dimos_cmd import run_dimos


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.slow
def test_hardware_stack_reports_status(dimos_stack_hw) -> None:
    assert_dimos_status_ok(run_dimos(["status"], timeout=45.0))
