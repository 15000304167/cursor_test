from __future__ import annotations


def assert_non_empty_text(text: str, *, label: str = "response") -> None:
    if not (text or "").strip():
        raise AssertionError(f"{label} is empty")


def assert_substrings(text: str, *needles: str) -> None:
    for n in needles:
        if n not in text:
            raise AssertionError(f"Expected {n!r} in text; got:\n{text[:2000]}")
