# 计划

## 目标与上下文

本轮让默认 `openharness update` 在强制同步后判断源码 commit 是否变化。判断点选在 `reset --hard @{u}` 前后读取本地 `HEAD`：如果同步后 `HEAD` 没变，说明本地源码已经是最新代码，跳过 `uv tool upgrade --reinstall openharness`；如果 `HEAD` 变化，再执行 reinstall。

`dev-source` 是开发者主动重装当前源码的模式，不参与 HEAD 变化判断，仍然总是 reinstall。

## 输入文档

- `requirements.md`

## 实施步骤

- [x] 增加 HEAD 读取和变化判断
  - 修改对象：`openharness_cli/commands/update.py`
  - 完成条件：强制同步前后通过 `git rev-parse HEAD` 获取 commit；读取失败时报错退出；`_force_sync` 返回是否变化。
  - 验证方式：单元测试模拟 `rev-parse` 输出相同和不同 commit。

- [x] 按变化决定是否 reinstall
  - 修改对象：`openharness_cli/commands/update.py`
  - 完成条件：`force-sync` 没有 commit 变化时不调用 `uv tool upgrade --reinstall openharness`，输出已经是最新代码；commit 变化时继续 reinstall。
  - 验证方式：测试断言 subprocess 调用序列和 stdout。

- [x] 同步兜底入口行为
  - 修改对象：`openharness_cli/main.py`
  - 完成条件：依赖缺失 fallback update 也通过 HEAD 变化决定是否 reinstall；无变化时不 reinstall；`dev-source` 仍总是 reinstall。
  - 验证方式：入口测试模拟调用序列。

- [x] 更新版本和证据
  - 修改对象：`pyproject.toml`、`uv.lock`、`evidence.md`
  - 完成条件：patch 版本提升；证据记录测试命令、覆盖表和残余风险。
  - 验证方式：全量测试通过，版本 diff 只包含本项目版本变化。

## 文件修改计划

- `openharness_cli/commands/update.py`：主 update 命令，承载 HEAD 读取、force-sync 变化判断和 reinstall 跳过逻辑。
- `openharness_cli/main.py`：依赖缺失时的 stdlib fallback，复制最小必要的 HEAD 判断逻辑。
- `tests/openharness_cases/test_cli_workflows.py`：主 update 行为测试。
- `tests/openharness_cases/test_entrypoint.py`：fallback update 行为测试。
- `pyproject.toml`、`uv.lock`：版本号。
- `docs/task-packages/update-skip-reinstall-when-current/evidence.md`：验证证据。

## 验证设计

必需命令：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py -v
```

预期结果：退出码 0；相关 update 和 entrypoint 测试全部通过。

```bash
uv run pytest tests/ -v
```

预期结果：退出码 0；全量测试通过。

边界场景：

- 强制同步前后 `HEAD` 相同时跳过 reinstall。
- 强制同步前后 `HEAD` 不同时执行 reinstall。
- `dev-source` 不受 HEAD 判断影响，仍执行 reinstall。
- fallback update 同步失败或 HEAD 读取失败不继续 reinstall。

## 进度记录

- [x] 需求已写入。
- [x] 计划已写入并进入实现。
- [x] 代码和测试已完成。
- [x] 验证通过并归档。

## 决策与发现

- 判断点选择 `reset` 前后的 `HEAD`，不是 `fetch` 输出。原因是 `fetch` 只更新远端引用，本地源码是否变化由 reset 后的本地 `HEAD` 决定。

## 风险接受

- 不检查已安装工具是否损坏。接受理由：本轮目标是“源码没变就不 reinstall”，本地安装修复可通过 `dev-source` 主动重装。
- 不新增 `--force-reinstall`。接受理由：当前已有 `dev-source` 能满足开发者主动重装场景。

## 完成判定

- 默认 update 在源码 commit 未变化时提示已经是最新代码，并跳过 reinstall。
- 默认 update 在源码 commit 变化时继续 reinstall。
- fallback 入口行为一致。
- `dev-source` 仍总是 reinstall。
- 相关测试和全量测试通过。
