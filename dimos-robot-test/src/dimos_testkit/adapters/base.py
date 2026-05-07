from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult


class DimosStackAdapter(ABC):
    """Abstract stack lifecycle + skill invocation surface for tests."""

    @abstractmethod
    def start(self) -> None:
        """Start blueprint (or no-op if DIMOS_SKIP_STACK)."""

    @abstractmethod
    def stop(self) -> None:
        """Stop blueprint / dimos process."""

    @abstractmethod
    def wait_ready(self, timeout_s: float = 120.0) -> None:
        """Block until stack reports skills / healthy MCP."""

    @abstractmethod
    def get_run_id(self) -> str | None:
        """Parse ``dimos status`` run id if available."""

    @abstractmethod
    def call_skill(self, name: str, args: dict[str, Any] | None = None) -> DimosCmdResult:
        """Invoke a skill by name (default: MCP CLI)."""

    @property
    @abstractmethod
    def profile_name(self) -> str:
        ...
