from __future__ import annotations

from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult


def assert_dimos_status_ok(result: DimosCmdResult) -> None:
    if not result.ok:
        raise AssertionError(f"dimos status failed ({result.returncode}): {result.stderr}\n{result.stdout}")
