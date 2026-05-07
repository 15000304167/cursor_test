from __future__ import annotations

import ipaddress
import os
from typing import Any

import yaml

from dimos_testkit.paths import configs_dir


def load_safety_config() -> dict[str, Any]:
    path = configs_dir() / "safety.yaml"
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def assert_hardware_allowed() -> None:
    """Raise if hardware tests are not explicitly allowed in this environment."""
    cfg = load_safety_config()
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true" and cfg.get("ci_forbid_hardware", True):
        raise RuntimeError("Hardware tests are forbidden on GitHub Actions (configs/safety.yaml).")
    if os.environ.get("CI", "").lower() in {"1", "true", "yes"} and cfg.get("ci_forbid_hardware", True):
        if os.environ.get("ALLOW_CI_HARDWARE", "").lower() not in {"1", "true", "yes"}:
            raise RuntimeError("Hardware tests are forbidden when CI=1 unless ALLOW_CI_HARDWARE=1.")

    if os.environ.get("HARDWARE_TEST_ACK", "") != "I_UNDERSTAND":
        raise RuntimeError(
            'Set HARDWARE_TEST_ACK=I_UNDERSTAND to acknowledge real-robot risk before running.'
        )

    ip = os.environ.get("ROBOT_IP", "").strip()
    if not ip:
        raise RuntimeError("ROBOT_IP must be set for hardware tests.")

    prefixes: list[str] = list(cfg.get("allowed_robot_ip_prefixes") or [])
    if prefixes and not any(ip.startswith(p) for p in prefixes):
        raise RuntimeError(f"ROBOT_IP {ip!r} does not match allowed prefixes: {prefixes!r}")

    try:
        ipaddress.ip_address(ip.split("%")[0])
    except ValueError as e:
        raise RuntimeError(f"Invalid ROBOT_IP: {ip!r}") from e
