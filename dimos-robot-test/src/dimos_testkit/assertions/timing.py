from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def monotonic_elapsed(fn: Callable[[], T]) -> tuple[T, float]:
    """Return ``(result, elapsed_seconds)`` using monotonic clock."""
    t0 = time.monotonic()
    out = fn()
    return out, time.monotonic() - t0
