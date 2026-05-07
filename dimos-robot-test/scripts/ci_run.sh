#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
mkdir -p artifacts
export TEST_PROFILE="${TEST_PROFILE:-mcp_replay}"
exec pytest \
  -m "not hardware and not mujoco and not slow" \
  --junitxml=artifacts/junit.xml \
  tests/unit \
  tests/contract
