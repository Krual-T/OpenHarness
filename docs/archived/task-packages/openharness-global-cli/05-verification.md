# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py`，锁定正式包入口与 `project.scripts` 配置。
  - 再执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py` 与 `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py`，确认文档与现有 CLI 行为都没有回归。
  - 再执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认路径迁移没有破坏 task package 协议。
  - 最后执行 `uv tool install --editable /home/Shaokun.Tang/Projects/openharness --force` 与 `openharness bootstrap`，确认真实安装后能得到可执行命令。
- Executed Path:
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py`，结果为 2 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`，结果为 41 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py`，结果为 13 passed。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，结果为通过，校验了 29 个 task package。
  - 已执行 `uv tool install --editable /home/Shaokun.Tang/Projects/openharness --force`，安装输出包含 `Installed 1 executable: openharness`。
  - 已执行 `openharness bootstrap`，确认全局命令可直接读取 manifest 并列出 active task packages。
- Path Notes:
  - 本轮没有额外做跨平台 PATH 手工验证，但已经通过 `uv tool install` 的真实安装输出和本机直接执行 `openharness bootstrap` 证明 Linux 环境下主路径成立。
  - `check-tasks` 初次执行暴露了 archived task package 中的旧路径引用，本轮已一并修正并重新验证通过。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py`
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 入口测试证明仓库根存在正式 `openharness_cli` 包，且 `pyproject.toml` 暴露 `openharness = "openharness_cli.main:main"`。
- 协议文档测试证明安装文档已包含 `uv tool install --editable`、`openharness bootstrap` 和已安装用户迁移说明。
- CLI 工作流测试证明现有命令行为没有因为入口调整而回归。
- `check-tasks` 通过，证明路径迁移没有留下断裂引用。
- 真实安装命令产出 `openharness` 可执行文件，随后 `openharness bootstrap` 可直接运行。

## Traceability
- 需求 1 和 2 由 `test_entrypoint.py`、`uv tool install --editable ... --force` 输出和 `openharness bootstrap` 共同覆盖，证明全局命令存在且不依赖业务项目 `pyproject.toml`。
- 需求 3 由 `test_cli_workflows.py` 与 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 覆盖，证明旧脚本入口仍可执行。
- 需求 4 和 5 由 `test_protocol_docs.py` 与更新后的 `INSTALL.codex.md` 覆盖，证明文档说明新装与已安装用户路径，并推荐 `uv tool install --editable`。

## Risk Acceptance
- 当前接受“未在 Windows 和 macOS 真实终端中执行安装验证”这一残余风险，因为本轮目标是先建立仓库级可安装命令与文档主路径，且安装方式完全基于 `uv tool` 的官方行为。
- 若后续出现跨平台 PATH、可执行入口或 editable 安装差异，再单独开 task package 为平台验证与补充说明建证据。

## Latest Result
- 最近一次验证已通过。入口测试、协议文档测试、CLI 工作流测试、`check-tasks` 和真实安装命令都返回成功；`openharness bootstrap` 已可直接使用。
- Latest Artifact:
  - `docs/archived/task-packages/openharness-global-cli/05-verification.md`
