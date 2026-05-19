# 详细设计

## 可观察性与验证准备

- **验证路径**（主路径）：在新项目中运行 `install.sh <dir>` → 检查 symlink 是否正确解析 → 检查 `.claude/settings.json` 是否含 SessionStart hook → 重复运行确认幂等
- **降级路径**：如无 Claude Code 环境，只验证 Codex 路径的 symlink 创建；settings.json 损坏场景单独模拟
- **预期证据**：symlink 指向正确目标（`ls -la` 输出）、settings.json 内容（`cat` 输出）、幂等运行无报错（退出码 0）

## 新增或修改文件

| 文件 | 操作 | 原因 |
|------|------|------|
| `install.sh` | 新建 | 全局安装入口，clone + CLI 安装 + 调用 init |
| `openharness_cli/models/agent_type.py` | 新建 | 新增 AgentType 枚举，供 init 命令和后续扩展使用 |
| `openharness_cli/models/__init__.py` | 修改 | 导出 AgentType |
| `openharness_cli/commands/init_cmd.py` | 重写 | 承载全部项目级配置逻辑 |
| `openharness_cli/__init__.py` | 修改 | 导出 AgentType |

## 接口

### install.sh

```
install.sh <project-dir> [--branch <branch>]
```

- `<project-dir>`：必填，目标项目根目录
- `--branch/-b`：可选，指定 clone 的分支
- 退出码：0 成功，1 失败
- 不依赖任何环境变量

### openharness init --agent

```
openharness init --agent <claude|codex|all>
```

- `--agent`：可选，默认 `all`
- 接受值：`claude`、`codex`、`all`
- 不和已有 `--repo` 参数冲突（init 始终在 `ctx.obj.repo_root` 下操作）

### AgentType 枚举

```python
class AgentType(StrEnum):
    CLAUDE = "claude"
    CODEX = "codex"
    ALL = "all"
```

### SessionStart hook JSON 结构

```json
{
  "hooks": {
    "SessionStart": "using-openharness"
  }
}
```

合并策略：读取已有 settings.json → 保留所有字段 → `hooks` 不存在则创建 → `SessionStart` 不存在则写入 → `SessionStart` 已存在且值不同则跳过并警告

## 模块内部设计

### init_cmd.py

```
init(agent)                          ← 入口：参数校验 + 调度
  ├─ _ensure_clone_exists()          ← 验证 ~/.agents/skill-hub/openharness 存在
  ├─ _setup_claude(repo, clone)      ← Claude Code 平台配置
  │    ├─ symlink: .claude/skills/using-openharness → clone/skills/using-openharness
  │    └─ _write_session_start_hook(repo)
  ├─ _setup_codex(repo, clone)       ← Codex 平台配置
  │    └─ symlink: .agents/skills/openharness → clone/skills
  └─ _bridge_agent_files(repo, agent) ← AGENTS.md ↔ CLAUDE.md 桥接
```

职责分离：
- `init`：编排，不直接操作文件
- `_setup_claude` / `_setup_codex`：平台 symlink 创建，含冲突检测
- `_write_session_start_hook`：JSON 读取→合并→写入，独立可测试
- `_bridge_agent_files`：桥接逻辑，四象限判断

## 数据语义

### AgentType

三值枚举，对应 `--agent` 参数。`ALL` 表示同时配置两个平台。

### settings.json hook 格式

固定的顶层键 `hooks.SessionStart`，值为 skill 名字符串 `"using-openharness"`。不包含数组或命令格式。

### Symlink 路径

| 平台 | 链接路径 | 目标路径 |
|------|---------|---------|
| Claude | `<project>/.claude/skills/using-openharness` | `~/.agents/skill-hub/openharness/skills/using-openharness` |
| Codex | `<project>/.agents/skills/openharness` | `~/.agents/skill-hub/openharness/skills` |

### 桥接规则表

| AGENTS.md | CLAUDE.md | agent | 行为 |
|-----------|-----------|-------|------|
| 存在 | 不存在 | claude/all | `ln -s AGENTS.md CLAUDE.md` |
| 不存在 | 存在 | codex/all | `ln -s CLAUDE.md AGENTS.md` |
| 都存在 | — | any | 跳过，打印提示 |
| 都不存在 | — | any | 跳过 |

## 阶段门禁

实施前必须确定：
1. AgentType 枚举位置：`openharness_cli/models/agent_type.py`
2. SessionStart hook 写入目标：`.claude/settings.json`（非 settings.local.json）
3. Symlink 已存在指向正确目标 → 跳过；指向错误 → 删除重建并警告
4. init 非交互模式，所有冲突通过 stdout 警告传达

## 决策闭合

- **接受**：一份 install.sh + CLI init 分叉。理由：全局部分完全一致，维护成本最低
- **拒绝**：两份独立安装脚本。理由：唯一区别是 `--agent` 参数，拆分是过度设计
- **延期**：install.sh 支持 Windows Git Bash。触发条件：有 Windows 用户反馈后再处理

## 错误处理

| 场景 | 处理 |
|------|------|
| clone 目录不存在 | 打印 "未找到 OpenHarness 克隆，请先运行 install.sh"，退出码 1 |
| clone 存在但非 git repo | 打印 "路径存在但不是 git 仓库"，退出码 1 |
| settings.json JSON 损坏 | 打印 "settings.json 格式错误，请手动修复"，退出码 1 |
| Symlink 已存在且指向正确 | 跳过，静默 |
| Symlink 已存在且指向不同目标 | 删除后重建，打印警告 |
| SessionStart hook 已有其他值 | 不覆盖，打印 "SessionStart hook 已设置为 '<value>'，跳过" |
| 桥接时目标文件已存在（非 symlink） | 跳过，打印 "CLAUDE.md 已存在，跳过桥接" |

静默出错风险：
- `settings.json` 写入后不验证可读性 → 写入后立即 `json.load` 验证
- Symlink 创建后不验证目标可解析 → `ls -la <link>` 检查目标路径

## 迁移说明

本轮为全新功能，无迁移问题。实施顺序：
1. 新建 `agent_type.py`
2. 修改 `models/__init__.py` 和 `__init__.py` 导出
3. 重写 `init_cmd.py`
4. 新建 `install.sh`
5. 端到端验证

## 推荐图示

无需图示。

## 详细设计反思

- 验证策略：依赖手动在新项目中运行安装脚本，验证 symlink 和 settings.json。定性验证，可重复执行
- 接口边界：install.sh 和 init 命令的接口已精确到参数和退出码，足够编码
- 迁移假设：`~/.agents/skill-hub/openharness` 路径固定——如果未来需要支持自定义路径，需新增 `--clone-path` 参数
- 预期证据：symlink `ls -la` 输出 + settings.json `cat` 输出，两种证据即可判定成功
