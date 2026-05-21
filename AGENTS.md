# 项目事实地图

本文件是 OpenHarness 的仓库地图：告诉协作者事实来源在哪里、默认工作流是什么、完成任务时需要回写什么。

## 1. 仓库地图

### 事实来源优先级

1. `docs/task-packages/<task>/`
   - 活跃任务包的唯一事实来源；每个任务是一个独立 task package。
2. `docs/archived/task-packages/<task>/`
   - 已完成 task package 的归档区；保留历史事实与验证证据。
3. `docs/archived/legacy/`
   - 历史材料归档区；仅作为证据留存，不再作为当前任务事实源。
4. `docs/anti-patterns/`
   - 技能和模板撰写中反复出现的错误模式与自检清单。

### 源码目录

| 目录 | 说明 |
|------|------|
| `openharness/` | 核心库（`rwp.py` 运行时工作流包支持） |
| `openharness_cli/` | CLI 工具（`main.py` 入口，`cli.py` 路由，`commands/` 子命令，`core/` 核心逻辑，`models/` 数据模型） |
| `skills/using-openharness/` | 入口技能：`SKILL.md` 会话入口，`states/` 阶段技能，`references/` 模板与协议文档 |
| `tests/` | 测试（`openharness_cases/` 测试用例） |

### 配置与运行时目录

| 目录/文件 | 说明 |
|-----------|------|
| `.harness/` | OpenHarness 运行时状态（锁文件、RWP 实例） |
| `.claude/` | Claude Code 配置（`settings.json` 会话 Hook、`skills/` 技能链接） |
| `.agents/` | Agent 技能中枢（`skills/` 技能链接） |
| `.codex/` | Codex CLI 配置（`hooks.json`、`config.toml`） |
| `pyproject.toml` | Python 项目配置与依赖声明 |
| `uv.lock` | uv 依赖锁定文件 |

### 安装与入口

| 文件 | 说明 |
|------|------|
| `install.sh` | Linux / macOS 安装脚本 |
| `install.ps1` | Windows PowerShell 安装脚本 |
| `INSTALL.md` | 安装说明 |
| `README.md` | 项目概览与设计哲学 |

### 任务包协议

每个任务包放在 `docs/task-packages/<task>/`，固定包含：

- `task-info.yaml`：机器可读状态源。
- `requirements.md`：需求、目标、非目标、完成定义。
- `overview-design.md`：总体设计、边界、主数据流/状态流。
- `detailed-design.md`：详细设计，先写测试设计，再写实现落点、运行时验证方式与实施顺序。
- `verification-design.md`：验证方案与结果。
- `evidence.md`：落地证据、命令、剩余后续工作。

## 2. Python / uv 约定

- 仓库内 Python 相关命令统一使用 `uv run ...`。
- 工作流脚本依赖应写入 `pyproject.toml`，不要依赖会话里的临时安装。
- 只有明确的一次性临时场景才使用 `uv run --with ...`。

## 3. 提交要求

- 未经允许不得私自建立已经被忽略文件的 git 索引。
- 每次完成一轮可独立成立的改动后，都应进行一次 `git commit`。
- 提交粒度尽量聚焦；一个提交只解决一个明确问题。
- 提交信息应准确描述为什么改以及改了什么。
- 提交信息中不要包含 `Co-Authored-By` 尾部署名。

## 4. 信息输出要求

- 向用户展示、输出信息时，使用通俗易懂的中文表达，不写中英穿插的口号式短句。

如果用户当前任务与上述约定冲突，以用户明确要求为准。
