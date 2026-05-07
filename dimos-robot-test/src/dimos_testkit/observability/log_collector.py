from __future__ import annotations

from collections.abc import Callable

from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult, run_dimos


class LogCollector:
    """Capture ``dimos log`` output for failure triage."""

    def __init__(self, runner: Callable[..., DimosCmdResult] | None = None) -> None:
        self._run = runner or run_dimos

    def tail_text(self, n: int = 300) -> DimosCmdResult:
        return self._run(["log", "-n", str(n)], timeout=90.0)

    def tail_json(self, n: int = 300) -> DimosCmdResult:
        return self._run(["log", "-n", str(n), "--json"], timeout=90.0)

    def best_effort_bundle(self, n: int = 300) -> str:
        j = self.tail_json(n)
        if j.ok and j.stdout.strip():
            return j.stdout
        t = self.tail_text(n)
        return t.stdout if t.ok else (t.stderr or "")
