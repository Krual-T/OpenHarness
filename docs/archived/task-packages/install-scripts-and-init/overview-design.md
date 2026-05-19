# 总体设计

## 系统边界

**覆盖**：
- `install.sh`：一份全局安装脚本，clone/pull + CLI 安装，平台无关
- `openharness init --agent` 命令：按 `claude`/`codex`/`all` 分叉，完成项目级配置
- 新增 `AgentType` 枚举
- `.claude/settings.json` 的 SessionStart hook 写入
- AGENTS.md ↔ CLAUDE.md 桥接

**不覆盖**：
- Codex 的 hook 机制（Codex 靠 symlink 自动发现 skill）
- `.claude/settings.local.json`
- 已有 `.claude/settings.json` 中其他 hook 的迁移

## 推荐结构

两层架构：

```
install.sh                              ← 全局层：clone + CLI，仅此一份
openharness init --agent <type>         ← 项目层：symlink + hook + 桥接
```

模块划分：

- `install.sh`：bash 脚本，独立于 Python 包
- `openharness_cli/models/agent_type.py`：新增
- `openharness_cli/commands/init_cmd.py`：重写
  - `_setup_claude()`：symlink `.claude/skills/using-openharness` + SessionStart hook
  - `_setup_codex()`：symlink `.agents/skills/openharness`
  - `_bridge_agent_files()`：AGENTS.md ↔ CLAUDE.md 桥接

依赖方向：`install.sh` → `openharness init --agent` → 平台配置函数

## 关键流程

```
install.sh <project-dir>
  → 检查 git/uv
  → clone or pull ~/.agents/skill-hub/openharness
  → uv tool install --editable
  → openharness init --agent all <project-dir>
      → 创建 .harness/
      → [Claude]  symlink .claude/skills/using-openharness
      → [Claude]  SessionStart hook → .claude/settings.json
      → [Codex]   symlink .agents/skills/openharness
      → 桥接 AGENTS.md ↔ CLAUDE.md
```

关键失败点：
- clone 网络失败 → 退出，提示检查网络
- clone 目录存在但非 git repo → 退出，提示手动清理
- settings.json 损坏 → 报错，提示手动修复
- 已有冲突的 SessionStart hook → 不覆盖，警告

## 阶段门禁

进入 detailed_designing 前确定：
1. AgentType 枚举值和默认行为
2. SessionStart hook 的 JSON 结构和合并策略
3. 桥接规则四象限完整逻辑
4. symlink 冲突处理策略

## 取舍

**推荐方案**：一份 install.sh + CLI init 按 agent 分叉

收益：全局部分复用；init 用 Python 实现比 bash 更可靠；init 可独立运行（幂等修复）

代价：无显著代价

**备选方案（已拒绝）**：`install-codex.sh` + `install-claude.sh` 两份脚本

拒绝理由：clone 路径和 CLI 安装完全一致，唯一区别是最后的 `--agent` 参数，拆两份增加维护负担。

## 推荐图示

无需图示。

## 总体设计反思

**挑战**：init 命令是否交互式询问用户

结论：拒绝。init 保持非交互模式，冲突时打印警告继续执行。交互式提示在 CI/脚本场景会阻塞。
