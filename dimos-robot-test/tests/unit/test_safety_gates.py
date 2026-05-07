from __future__ import annotations

import pytest

from dimos_testkit.safety.gates import assert_hardware_allowed, load_safety_config


@pytest.mark.unit
def test_load_safety_config_has_bounds() -> None:
    cfg = load_safety_config()
    assert "velocity_forward_max_m_s" in cfg


@pytest.mark.unit
def test_hardware_requires_ack(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("ROBOT_IP", "192.168.1.10")
    monkeypatch.delenv("HARDWARE_TEST_ACK", raising=False)
    with pytest.raises(RuntimeError, match="HARDWARE_TEST_ACK"):
        assert_hardware_allowed()


@pytest.mark.unit
def test_github_actions_forbids_hardware(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("HARDWARE_TEST_ACK", "I_UNDERSTAND")
    monkeypatch.setenv("ROBOT_IP", "192.168.1.10")
    with pytest.raises(RuntimeError, match="forbidden"):
        assert_hardware_allowed()
