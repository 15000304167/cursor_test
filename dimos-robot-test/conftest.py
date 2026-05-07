from __future__ import annotations

import os
from pathlib import Path

import pytest

from dimos_testkit.adapters.hardware import HardwareStackAdapter
from dimos_testkit.adapters.stack_subprocess import StackSubprocessAdapter, active_profile_name
from dimos_testkit.cli_wrappers.dimos_cmd import which_dimos
from dimos_testkit.observability.artifacts import CaseArtifacts
from dimos_testkit.observability.log_collector import LogCollector
from dimos_testkit.paths import repo_root
from dimos_testkit.reporting.summary import write_session_summary


def _artifacts_root() -> Path:
    env = os.environ.get("TEST_ARTIFACTS_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return (repo_root() / "artifacts").resolve()


def _stack_ready_timeout_s() -> float:
    return float(os.environ.get("DIMOS_STACK_READY_TIMEOUT", "180"))


def _require_dimos_cli() -> None:
    require = os.environ.get("DIMOS_REQUIRE_CLI", "").lower() in {"1", "true", "yes"}
    if require and not which_dimos():
        pytest.skip("DIMOS_REQUIRE_CLI=1 but dimos not found on PATH")
    if not which_dimos():
        pytest.skip("dimos CLI not on PATH")


@pytest.fixture(scope="session")
def dimos_stack():
    """Start DimOS once per session for sim/replay integration tests."""
    if active_profile_name() == "hardware":
        pytest.skip("Use dimos_stack_hw when TEST_PROFILE=hardware")
    _require_dimos_cli()
    adapter = StackSubprocessAdapter()
    try:
        adapter.start()
        adapter.wait_ready(timeout_s=_stack_ready_timeout_s())
        yield adapter
    finally:
        adapter.stop()


@pytest.fixture(scope="session")
def dimos_stack_hw():
    """Hardware profile stack; skips immediately if TEST_PROFILE is not ``hardware``."""
    if active_profile_name() != "hardware":
        pytest.skip("Set TEST_PROFILE=hardware for hardware integration")
    _require_dimos_cli()
    adapter = HardwareStackAdapter()
    try:
        adapter.start()
        adapter.wait_ready(timeout_s=_stack_ready_timeout_s())
        yield adapter
    finally:
        adapter.stop()


@pytest.fixture
def case_artifacts(request) -> CaseArtifacts:
    return CaseArtifacts(_artifacts_root(), request.node.nodeid)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):  # type: ignore[name-defined]
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or not rep.failed:
        return
    arts: CaseArtifacts | None = item.funcargs.get("case_artifacts")  # type: ignore[assignment]
    if arts is None:
        return
    try:
        arts.append_meta({"failed_stage": "call", "longrepr": str(rep.longrepr)})
        lc = LogCollector()
        arts.write_text("dimos_log_tail.txt", lc.best_effort_bundle())
    except Exception as exc:  # noqa: BLE001
        arts.write_text("artifact_capture_error.txt", repr(exc))


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    root = _artifacts_root()
    root.mkdir(parents=True, exist_ok=True)
    write_session_summary(root / "summary.json", session, exitstatus)
