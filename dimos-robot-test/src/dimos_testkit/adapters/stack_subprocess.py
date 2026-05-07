from __future__ import annotations

import json
import os
import time
from typing import Any

import yaml

from dimos_testkit.adapters.base import DimosStackAdapter
from dimos_testkit.adapters.mcp_cli import McpCliAdapter
from dimos_testkit.cli_wrappers.dimos_cmd import DimosCmdResult, run_dimos, which_dimos
from dimos_testkit.paths import configs_dir


def load_profiles() -> dict[str, Any]:
    path = configs_dir() / "profiles.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def active_profile_name() -> str:
    return os.environ.get("TEST_PROFILE", "mcp_replay")


class StackSubprocessAdapter(DimosStackAdapter):
    """Start/stop DimOS via CLI subprocess; skills via :class:`McpCliAdapter`."""

    def __init__(self, profile: str | None = None) -> None:
        profiles = load_profiles()
        name = profile or active_profile_name()
        if name not in profiles:
            raise KeyError(f"Unknown profile {name!r}; known: {sorted(profiles)}")
        self._profile_key = name
        self._cfg: dict[str, Any] = profiles[name]
        self._mcp = McpCliAdapter()
        self._started = False

    @property
    def profile_name(self) -> str:
        return self._profile_key

    def _build_run_argv(self) -> list[str]:
        argv: list[str] = []
        for flag in self._cfg.get("extra_args") or []:
            argv.append(flag)
        argv.extend(["run", str(self._cfg["blueprint"])])
        if self._cfg.get("daemon"):
            argv.append("--daemon")
        mcp_port = self._cfg.get("mcp_port")
        env_port = os.environ.get("DIMOS_MCP_PORT")
        if env_port:
            argv.extend(["--mcp-port", env_port])
        elif mcp_port:
            argv.extend(["--mcp-port", str(mcp_port)])
        if self._cfg.get("requires_robot_ip"):
            ip = os.environ.get("ROBOT_IP")
            if not ip:
                raise RuntimeError("ROBOT_IP is required for hardware profile")
            argv.extend(["--robot-ip", ip])
        return argv

    def start(self) -> None:
        if os.environ.get("DIMOS_SKIP_STACK", "").lower() in {"1", "true", "yes"}:
            self._started = True
            return
        if not which_dimos():
            raise RuntimeError("dimos CLI not found on PATH")
        argv = self._build_run_argv()
        r = run_dimos(argv, timeout=30.0)
        if not r.ok:
            raise RuntimeError(f"dimos start failed ({r.returncode}): {r.stderr}\n{r.stdout}")
        self._started = True

    def stop(self) -> None:
        if not which_dimos():
            return
        run_dimos(["stop"], timeout=60.0)
        self._started = False

    def wait_ready(self, timeout_s: float = 120.0) -> None:
        deadline = time.monotonic() + timeout_s
        last_err = ""
        while time.monotonic() < deadline:
            st = self._mcp.status_raw()
            if st.ok and st.stdout.strip():
                if "skill" in st.stdout.lower() or "mcp" in st.stdout.lower():
                    return
            lt = self._mcp.list_tools_raw()
            if lt.ok and lt.stdout.strip():
                try:
                    names = self._mcp.list_tool_names()
                    if names:
                        return
                except Exception as e:  # noqa: BLE001
                    last_err = str(e)
            time.sleep(1.5)
        raise TimeoutError(f"stack not ready within {timeout_s}s; last={last_err!r}")

    def get_run_id(self) -> str | None:
        r = run_dimos(["status"], timeout=30.0)
        if not r.ok:
            return None
        text = r.stdout.strip()
        if text.startswith("{"):
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    for k in ("run_id", "id", "runId"):
                        v = data.get(k)
                        if v is not None:
                            return str(v)
            except json.JSONDecodeError:
                pass
        for line in text.splitlines():
            lower = line.lower()
            if "run" in lower and ":" in line:
                rhs = line.split(":", 1)[1].strip()
                token = rhs.split()[0] if rhs else ""
                if token:
                    return token
        return None

    def call_skill(self, name: str, args: dict[str, Any] | None = None) -> DimosCmdResult:
        return self._mcp.call_skill(name, args)
