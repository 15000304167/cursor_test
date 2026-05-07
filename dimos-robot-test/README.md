# DimOS 机器人功能自动化测试框架

基于 [dimensionalOS/dimos](https://github.com/dimensionalOS/dimos) 的分层测试：**单元**、**契约（MCP 工具列表/Schema）**、**仿真或回放集成**、**真机集成**（闸门保护）。

## 快速开始

```bash
cd dimos-robot-test
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -m unit
```

若暂未 `pip install -e`，可临时：

```bash
cd dimos-robot-test
PYTHONPATH=src pytest -m unit
```

集成测试需本机已安装 `dimos` 且可启动蓝图；或先手动 `dimos --replay run unitree-go2-agentic-mcp --daemon` 后设 `DIMOS_SKIP_STACK=1`。

```bash
export TEST_PROFILE=mcp_replay
pytest -m "integration and not hardware" --timeout=600
```

真机（默认不会在 CI 执行）：

```bash
export TEST_PROFILE=hardware
export HARDWARE_TEST_ACK=I_UNDERSTAND
export ROBOT_IP=192.168.123.161
pytest tests/integration_hardware -m hardware --timeout=1200
```

## 配置

- [configs/profiles.yaml](configs/profiles.yaml)：蓝图与 CLI 模板。
- [configs/safety.yaml](configs/safety.yaml)：真机参数上限。
- [.env.example](.env.example)：环境变量说明。

## CI

`.github/workflows/ci.yml` 运行 `scripts/ci_run.sh`（仅 `unit` + `contract`，不启硬件、不启 mujoco）。

## 目录说明

- `src/dimos_testkit/`：适配器、断言、观测、报告、安全闸门。
- `tests/`：按分层组织的用例。
- `fixtures/tools_golden.json`：MCP 工具名快照（按项目维护）。
