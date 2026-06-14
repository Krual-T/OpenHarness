# 计划

## 目标与上下文

本轮把 `openharness update` 的默认行为从 `git pull` 改为强制同步：`git fetch --prune` 后 `git reset --hard @{u}`，再 reinstall。新增 `dev-source` 模式给 OpenHarness 仓库开发者使用，它跳过 git 同步，只从当前安装来源目录重新安装。

相关代码集中在 `openharness_cli/commands/update.py` 和依赖缺失兜底入口 `openharness_cli/main.py`。已有同步命令重试和失败详情输出应继续复用。

## 输入文档

- `requirements.md`

## 实施步骤

- [x] 调整主 update 命令模式
  - 修改对象：`openharness_cli/commands/update.py`
  - 完成条件：`UpdateMode` 支持 `force-sync` 和 `dev-source`；无参数默认解析为 `force-sync`；`--force-sync` 保持可用；`--mode dev-source` 跳过 git 同步。
  - 验证方式：单元测试断言默认调用 `git fetch --prune`、`git reset --hard @{u}`、`uv tool upgrade --reinstall openharness`；`dev-source` 只调用 reinstall。

- [x] 调整默认模式配置
  - 修改对象：`openharness_cli/commands/update.py`
  - 完成条件：`--set-default-mode dev-source` 可保存；读取非法模式时报错提示包含 `force-sync` 和 `dev-source`；旧的 `pull` 不再作为有效目标模式。
  - 验证方式：单元测试覆盖保存 `dev-source` 和非法配置提示。

- [x] 调整依赖缺失兜底入口
  - 修改对象：`openharness_cli/main.py`
  - 完成条件：无参数 fallback update 执行强制同步；`--dev-source` 或 `--mode dev-source` fallback update 跳过 git 同步；同步失败仍重试 3 次并阻断 reinstall。
  - 验证方式：入口测试模拟 subprocess 调用序列。

- [x] 更新文档说明
  - 修改对象：`INSTALL.md`、`README.md`、必要的 CLI 参考文档
  - 完成条件：文档说明默认更新会强制同步安装源码目录；开发本仓库时使用 `dev-source`；不再推荐设置默认 `force-sync`。
  - 验证方式：现有协议文档测试和人工 diff 检查。

- [x] 提升版本并记录证据
  - 修改对象：`pyproject.toml`、`uv.lock`、`evidence.md`
  - 完成条件：版本号按不兼容行为变更提升到下一主版本；证据记录命令结果、覆盖表和残余风险。
  - 验证方式：全量测试通过，git diff 确认版本一致。

## 文件修改计划

- `openharness_cli/commands/update.py`：主 CLI 更新命令；负责模式枚举、默认模式解析、同步命令执行、reinstall。
- `openharness_cli/main.py`：依赖缺失时的 stdlib 兜底入口；保持不依赖 Typer，同时实现新的默认强制同步和 `dev-source`。
- `tests/openharness_cases/test_cli_workflows.py`：主 update 命令行为测试。
- `tests/openharness_cases/test_entrypoint.py`：CLI 入口和 fallback update 测试。
- `INSTALL.md`：安装和更新说明的主要用户入口。
- `README.md`、`skills/using-openharness/references/cli-reference.md`：命令摘要说明。
- `pyproject.toml`、`uv.lock`：版本号。
- `docs/task-packages/update-force-sync-dev-source/evidence.md`：验证证据。

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

- 默认无参数不再调用 `git pull`。
- `dev-source` 不调用任何 git 同步命令。
- fallback update 在同步失败三次后不执行 reinstall。

## 进度记录

- [x] 需求已写入。
- [x] 计划已写入并进入实现。
- [x] 代码和测试已完成。
- [ ] 验证通过并归档。

## 决策与发现

- 默认强制同步是有破坏性的行为变更，会丢弃安装源码目录的本地改动，因此按不兼容变更提升主版本。
- `dev-source` 表达开发者“只 reinstall 当前来源目录”的需求，不承担任意路径安装职责。

## 风险接受

- 不实现 release/tag 更新。接受理由：这需要发布渠道设计，不属于本轮 CLI 同步策略调整。
- 不支持选择任意 branch。接受理由：本轮沿用 `@{u}`，保持行为简单且可测。

## 完成判定

- 默认 update 执行强制同步再 reinstall。
- `dev-source` 跳过 git 同步并 reinstall。
- 主入口和 fallback 入口行为一致。
- 文档说明新的默认行为和开发者模式。
- 相关测试和全量测试通过。
