#!/usr/bin/env bash
set -euo pipefail
PROFILE="${TEST_PROFILE:-mcp_replay}"
case "${PROFILE}" in
  mcp_replay)
    exec dimos --replay run unitree-go2-agentic-mcp --daemon
    ;;
  sim)
    exec dimos --simulation run unitree-g1-agentic-sim --daemon
    ;;
  hardware)
    : "${ROBOT_IP:?Set ROBOT_IP for hardware profile}"
    exec dimos run unitree-go2-agentic-mcp --robot-ip "${ROBOT_IP}" --daemon
    ;;
  *)
    echo "Unknown TEST_PROFILE=${PROFILE} (expected mcp_replay|sim|hardware)" >&2
    exit 1
    ;;
esac
