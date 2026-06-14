# Evidence

## 已完成

- 在 `AGENTS.md` 开头新增项目介绍。
- 明确 OpenHarness 的项目组成：核心库、CLI、技能、文档和测试。
- 明确当前仓库内 `skills/using-openharness/` 与环境注入的 `using-openharness` 的区别。
- 明确系统安装的 OpenHarness 通常落后于当前项目源码；更新系统安装版本时不能在本仓库目录运行 `openharness update`，必须切到其他目录。
- 将项目版本从 `3.0.3` 提升到 `3.0.4`，并同步 `uv.lock`。

## 验证

- `AGENTS.md` 仍保留仓库协作入口、仓库地图路由、`using-openharness` 技能入口和提交要求。
- `pyproject.toml` 和 `uv.lock` 均同步到 `3.0.4`。

## 命令结果

- `uv run pytest tests/openharness_cases/test_protocol_docs.py::test_agents_md_routes_repo_skill_usage_through_openharness -v`
  - 结果：退出码 0；1 项通过。
- `rg -n 'OpenHarness 是|系统安装|openharness update|skills/using-openharness|using-openharness|3\.0\.4' AGENTS.md pyproject.toml uv.lock`
  - 结果：退出码 0；命中项目介绍、系统安装说明、更新禁忌、技能入口和版本号。
- `uv run pytest tests/ -v`
  - 结果：退出码 0；73 项通过。

## 变更文件

- `AGENTS.md`：新增项目介绍和系统安装版本说明。
- `pyproject.toml`：项目版本更新到 `3.0.4`。
- `uv.lock`：同步项目自身版本到 `3.0.4`。
- `docs/task-packages/agents-project-introduction/`：记录本轮需求和证据。

## 语义审核

- `AGENTS.md` 开头说明了 OpenHarness 是面向智能体协作的仓库脚手架和工作流工具。
- 项目组成覆盖核心库、CLI、技能、文档和测试。
- 文案明确区分仓库内 `skills/using-openharness/` 和环境注入的 `using-openharness`。
- 文案明确禁止在本仓库目录运行 `openharness update` 来更新系统安装版本。

## 验证结果

最终结论：通过。

## 残余风险

- 本轮未新增字符级测试断言项目介绍的完整措辞。接受理由：该段是自然语言说明，已有现有协议测试保护 `using-openharness` 入口，关键词检查覆盖了本轮关键事实。

## Reflection

### Skill

本次使用 `using-openharness` 后仍需要手工判断任务规模；这类单文件说明补充适合走 `mechanical`，不需要展开计划阶段。
