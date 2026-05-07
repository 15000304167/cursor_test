from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class DimosCmdResult:
    stdout: str
    stderr: str
    returncode: int

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def which_dimos() -> str | None:
    return shutil.which("dimos")


def run_dimos(
    args: Sequence[str],
    *,
    timeout: float | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | os.PathLike[str] | None = None,
) -> DimosCmdResult:
    """Run ``dimos`` CLI with unified timeout and UTF-8 capture."""
    cmd = ["dimos", *args]
    merged: dict[str, str] = {**os.environ, **dict(env or {})}
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=merged,
            cwd=cwd,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if isinstance(e.stdout, str) else ""
        err = (e.stderr or "") if isinstance(e.stderr, str) else ""
        err = f"{err}\n[dimos_testkit] timeout after {timeout}s: {' '.join(cmd)}"
        return DimosCmdResult(stdout=out, stderr=err, returncode=124)
    return DimosCmdResult(
        stdout=proc.stdout or "",
        stderr=proc.stderr or "",
        returncode=int(proc.returncode),
    )
