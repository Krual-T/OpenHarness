# Evidence

## 已完成

- 重写 `AGENTS.md` 为仓库协作入口，并保留提交要求。
- 新增 `docs/repo_map/` 根层和 `docs`、`source`、`skills`、`config`、`tests` 入口地图。
- 按用户给出的 NG 反模式内容新增 `docs/anti-patterns/repo-map.md`。
- 将 `pyproject.toml` 的 `project.version` 从 `3.0.2` 提升到 `3.0.3`。

## 验证

- 检查 `docs/repo_map/` 下所有 `MAP.md` 只包含 `# 标题` 和 `## 目录作用`。
- 检查地图内容未纳入未被 Git 记录的本地运行态目录。

## 命令结果

- `find docs/repo_map -name MAP.md -print -exec sed -n '1,80p' {} \;`
  - 结果：退出码 0；列出 6 个 `MAP.md`，均只有 `# 标题`、`## 目录作用` 和目录作用列表。
- `test "$(find docs/repo_map -name MAP.md -exec sh -c 'printf "%s:" "$1"; rg "^## " "$1" | wc -l' sh {} \; | awk -F: '$2 != 1 {print}' | wc -l)" -eq 0 && echo 'MAP section check passed'`
  - 结果：退出码 0；输出 `MAP section check passed`。
- `rg -n '\.(codex|agents|claude|harness|tmp|venv|vscode)/|__pycache__|pytest_cache|容器' docs/repo_map AGENTS.md docs/anti-patterns/repo-map.md || true`
  - 结果：退出码 0；无命中。
- `rg -n '^version = "3\.0\.3"|name = "openharness"' pyproject.toml uv.lock`
  - 结果：退出码 0；`pyproject.toml` 和 `uv.lock` 均显示 `openharness` 版本为 `3.0.3`。
- `uv run pytest tests/openharness_cases/test_protocol_docs.py::test_agents_md_routes_repo_skill_usage_through_openharness -v`
  - 结果：退出码 0；1 项通过。
- `uv run pytest tests/ -v`
  - 结果：退出码 0；73 项通过。

## 变更文件

- `AGENTS.md`：重写为仓库协作入口，保留提交要求和版本号规则。
- `docs/anti-patterns/repo-map.md`：新增仓库地图反模式，采用用户给出的 NG 反模式内容。
- `docs/repo_map/MAP.md`：新增仓库地图根层。
- `docs/repo_map/docs/MAP.md`：新增长期文档地图。
- `docs/repo_map/source/MAP.md`：新增 Python 源码地图。
- `docs/repo_map/skills/MAP.md`：新增 OpenHarness 技能地图。
- `docs/repo_map/config/MAP.md`：新增安装和项目配置地图。
- `docs/repo_map/tests/MAP.md`：新增测试入口地图。
- `pyproject.toml`：将 `project.version` 从 `3.0.2` 提升到 `3.0.3`。
- `uv.lock`：同步项目自身版本号。
- `docs/task-packages/agents-entry-and-repo-map-routing/`：记录本轮需求、计划和证据。

## 语义审核

- `AGENTS.md` 已从完整仓库事实地图改为协作入口，稳定入口路由指向 `docs/repo_map/`。
- `AGENTS.md` 保留了提交要求，包括每轮独立改动提交、提交前更新 `pyproject.toml` 版本号、不添加 `Co-Authored-By`。
- `AGENTS.md` 保留 `using-openharness` 技能入口，满足仓库既有协议测试。
- `docs/repo_map/` 采用 OpenHarness 自身结构：`docs`、`source`、`skills`、`config`、`tests`。
- 所有 `MAP.md` 只保留 `# 标题` 和 `## 目录作用`。

### 子智能体审核

- `AGENTS.md`：通过。子智能体确认其已改为仓库协作入口，没有继续承载完整仓库百科。
- 提交要求保留情况：通过。子智能体确认 `AGENTS.md` 保留提交要求，并明确提交前修改 `pyproject.toml` 的 `project.version`。
- `docs/anti-patterns/repo-map.md`：通过。子智能体确认内容基本采用用户给出的 NG 反模式规范，并明确 `MAP.md` 只能有 `# 标题` 和 `## 目录作用`。
- `docs/repo_map/` 是否贴合 OpenHarness：有条件通过。子智能体确认正式地图已使用 `docs`、`source`、`skills`、`config`、`tests`，但发现工作区还残留空目录 `docs/repo_map/server/` 和 `docs/repo_map/ops/`。
- `MAP.md` 结构和边界：通过。子智能体确认所有 `MAP.md` 只有一个 `#` 标题和一个 `## 目录作用`，未纳入本地运行态目录。
- 任务包记录：通过。子智能体确认需求、计划、证据和状态与本轮实际改动一致。

### 人类审阅反馈

- 用户指出 `docs`、`server`、`ops`、`tests` 是从其他仓库复制来的示例，需要根据 OpenHarness 项目调整。
- 已采纳：正式路由调整为 `docs`、`source`、`skills`、`config`、`tests`。
- 已闭合：删除子智能体指出的空目录 `docs/repo_map/server/` 和 `docs/repo_map/ops/`。

## 验收覆盖

| 验收项 | 证据 | 结论 |
|--------|------|------|
| `AGENTS.md` 是仓库协作入口 | `AGENTS.md` 章节为读取顺序、稳定入口路由、工程风格、Python 和 uv 约定、提交要求、Reflection、信息输出要求 | 通过 |
| 提交要求保留 | `AGENTS.md` 保留提交要求，`pyproject.toml` 更新为 `3.0.3` | 通过 |
| OpenHarness 技能入口保留 | `AGENTS.md` 包含 `using-openharness` 技能入口 | 通过 |
| 新增渐进式仓库地图 | `docs/repo_map/` 包含根层和 `docs`、`source`、`skills`、`config`、`tests` 入口地图 | 通过 |
| 地图符合 NG 反模式 | 结构检查输出 `MAP section check passed`，关键词检查无命中 | 通过 |
| 路由贴合 OpenHarness | 用户指出后已移除 `server`、`ops` 正式路由，并删除空目录 | 通过 |

## 验证结果

最终结论：通过。

子智能体审核和人类反馈不存在未闭合分歧。子智能体提出的空目录残留问题已处理；用户提出的路由应按 OpenHarness 调整的问题已处理。完整测试已通过。

## 残余风险

- 本轮没有为自然语言文档新增 pytest 字符串断言。接受理由：验证对象是协作协议和地图语义，字符级断言会让正常改写被误判为失败。

## 后续事项

- 后续如果继续细分 `docs/repo_map/`，需要先查看 `docs/anti-patterns/repo-map.md`，并保持每层 `MAP.md` 只说明下一层目录或直接文件的作用。

## Reflection

### Skill

本次使用 `using-openharness` 后发现：需求阶段要求用户确认后再继续，但用户给出的改写内容已经非常具体，且后续中断补充了“提交要求要保留”和 NG 反模式正文。这里将这些明确输入直接写入任务包，避免把已经确认的文本再口头重复一遍。

### Map

本次新增 `docs/repo_map/` 后，用户补充了更严格的地图反模式规则。已按该规则收缩所有 `MAP.md`，删除多余 section、越级说明和未被 Git 记录的本地目录引用。用户指出 `server`、`ops` 是其他仓库复制来的路由后，已调整为贴合 OpenHarness 的 `source`、`skills`、`config`。
