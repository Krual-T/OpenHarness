# 计划

## 目标与上下文

本轮把仓库根部的 `AGENTS.md` 从完整事实地图改为协作入口，并新增 `docs/repo_map/` 渐进式地图。用户已明确要求保留提交要求，并提供了 `docs/anti-patterns/repo-map.md` 的 NG 反模式正文。用户后续指出 `server`、`ops`、`tests` 是从其他仓库复制来的示例，需要调整为 OpenHarness 自己的项目结构。

## 输入文档

- `requirements.md`：本轮交付物、非目标和约束。
- 用户补充的 NG 反模式正文：作为 `docs/anti-patterns/repo-map.md` 的事实输入。

## 实施步骤

- [x] 重写仓库协作入口
  - 修改对象：`AGENTS.md`
  - 完成条件：文件说明读取顺序、稳定入口路由、工程风格、Python 和 uv 约定、提交要求、Reflection 和信息输出要求。
  - 验证方式：人工审阅 `AGENTS.md` 是否保留提交要求，并且不再复制完整仓库地图。

- [x] 新增仓库地图反模式
  - 修改对象：`docs/anti-patterns/repo-map.md`
  - 完成条件：内容采用用户给出的 NG 反模式正文。
  - 验证方式：人工比对用户输入，确认核心规范、反模式和修正方式均已覆盖。

- [x] 新增渐进式仓库地图
  - 修改对象：`docs/repo_map/MAP.md`、`docs/repo_map/docs/MAP.md`、`docs/repo_map/source/MAP.md`、`docs/repo_map/skills/MAP.md`、`docs/repo_map/config/MAP.md`、`docs/repo_map/tests/MAP.md`
  - 完成条件：每个 `MAP.md` 只包含 `# 标题` 和 `## 目录作用`，并只说明下一层目录或直接文件的作用。
  - 验证方式：运行结构检查命令，确认每个地图文件只有一个二级标题；人工审阅地图未写入未被 Git 记录的本地目录。

- [x] 更新版本和任务包证据
  - 修改对象：`pyproject.toml`、`uv.lock`、本任务包文档。
  - 完成条件：`project.version` 从 `3.0.2` 提升到 `3.0.3`，`uv.lock` 同步项目自身版本号，任务包记录需求、计划和证据。
  - 验证方式：查看版本差异和任务包文件。

## 文件修改计划

- `AGENTS.md`：仓库协作入口，承载稳定路由和仓库级规则。
- `docs/anti-patterns/repo-map.md`：仓库地图维护反模式和修正方式。
- `docs/repo_map/MAP.md`：仓库地图根层。
- `docs/repo_map/docs/MAP.md`：长期文档地图。
- `docs/repo_map/source/MAP.md`：Python 源码地图。
- `docs/repo_map/skills/MAP.md`：OpenHarness 技能地图。
- `docs/repo_map/config/MAP.md`：安装和项目配置地图。
- `docs/repo_map/tests/MAP.md`：测试入口地图。
- `docs/task-packages/agents-entry-and-repo-map-routing/`：本轮任务包记录。
- `pyproject.toml`：提交前版本号。
- `uv.lock`：项目自身版本号同步。

## 验证设计

- 主要验证方式：定性审核，辅以结构检查命令。
- 必需命令：
  - `find docs/repo_map -name MAP.md -print -exec sed -n '1,80p' {} \;`
  - `test "$(find docs/repo_map -name MAP.md -exec sh -c 'printf "%s:" "$1"; rg "^## " "$1" | wc -l' sh {} \; | awk -F: '$2 != 1 {print}' | wc -l)" -eq 0 && echo 'MAP section check passed'`
  - `rg -n '\.(codex|agents|claude|harness|tmp|venv|vscode)/|__pycache__|pytest_cache|容器' docs/repo_map AGENTS.md docs/anti-patterns/repo-map.md || true`
- 预期结果：地图结构检查输出 `MAP section check passed`；本地运行态目录和误导性“容器”描述没有命中。
- 边界场景：`AGENTS.md` 可说明稳定入口用途，但 `docs/repo_map/` 不应纳入未被 Git 记录的本地运行态目录。

### 审核矩阵

| 审核对象 | 审核维度 | 通过标准 | 证据要求 |
|----------|----------|----------|----------|
| `AGENTS.md` | 入口职责 | 只做仓库协作入口，保留提交要求和版本号规则 | 人工审阅对应章节 |
| `docs/anti-patterns/repo-map.md` | 用户输入一致性 | 覆盖用户给出的正向规范、反模式和修正方式 | 人工比对用户输入 |
| `docs/repo_map/` | 地图结构 | 每个 `MAP.md` 只包含 `# 标题` 和 `## 目录作用` | 结构检查命令输出 |
| `docs/repo_map/` | 地图边界 | 不纳入未被 Git 记录的本地运行态目录，不越级展开普通文件细节 | 人工审阅和关键词检查 |

## 进度记录

- 已完成 `AGENTS.md` 重写。
- 已按用户给出的 NG 反模式正文替换 `docs/anti-patterns/repo-map.md`。
- 已收缩所有 `MAP.md`，删除多余 section、越级说明和本地目录引用。
- 已将从其他仓库复制来的 `server`、`ops` 路由调整为 OpenHarness 的 `source`、`skills`、`config` 路由。

## 决策与发现

- 采用 `docs/repo_map/`，因为用户草稿已使用该路径，语义明确。
- 采用 `docs/anti-patterns/repo-map.md`，与仓库既有 `docs/anti-patterns/` 目录命名保持一致，避免新增 `docs/anti_patterns/`。
- `uv.lock` 的变化仅为项目自身版本号同步，不是依赖漂移。

## 风险接受

- 本轮不新增 pytest，因为主要验证对象是自然语言协议和地图边界，字符级断言容易把正常改写误判为失败。
- 本轮只建立根层和贴合 OpenHarness 当前结构的一层入口地图，不继续拆分更深层地图；后续只有在实际阅读成本变高时再新增下一层 `MAP.md`。

## 完成判定

- 进入实现的条件：本计划覆盖全部交付物，并给出结构检查和定性审核矩阵。
- 实现完成的条件：所有计划中的文件已落地，版本号已更新。
- 验证完成的条件：结构检查通过，关键词检查无误导性命中，差异审阅确认提交要求保留且地图遵守 NG 反模式。
