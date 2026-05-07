from __future__ import annotations

from typing import Any

from dimos_testkit.adapters.stack_subprocess import StackSubprocessAdapter
from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult
from dimos_testkit.safety.gates import assert_hardware_allowed


class HardwareStackAdapter(StackSubprocessAdapter):
    """Real-robot profile with mandatory safety gates before start."""

    def __init__(self) -> None:
        super().__init__(profile="hardware")

    def start(self) -> None:
        assert_hardware_allowed()
        super().start()

    def call_skill(self, name: str, args: dict[str, Any] | None = None) -> DimosCmdResult:
        assert_hardware_allowed()
        return super().call_skill(name, args)
