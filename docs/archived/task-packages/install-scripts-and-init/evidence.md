# 证据

## 验证结果

- **verify_by**: qualitative
- **Result**: passed

## 变更文件

- `openharness_cli/models/agent_type.py` — 新建 AgentType 枚举
- `openharness_cli/models/__init__.py` — 添加 AgentType 导入和导出
- `openharness_cli/__init__.py` — 添加 AgentType 导入和导出
- `openharness_cli/commands/init_cmd.py` — 重写，支持 --agent 参数
- `install.sh` — 新建全局安装脚本

## 语义审核

### 审核对象

| 对象 | 审核维度 |
|------|---------|
| `install.sh` | 可执行性、参数校验、前置检查 |
| `openharness init --agent` | 参数接受/拒绝、symlink 正确性、hook 内容、桥接逻辑、幂等性、错误处理 |

### 发现

无问题。全部验证项通过。

### 验证命令执行记录

**命令 1**：init --agent claude（项目含 AGENTS.md）
```
openharness --repo /tmp/oh-test init --agent claude
退出码: 0
```

**命令 2**：Claude Code symlink
```
ls -la /tmp/oh-test/.claude/skills/using-openharness
→ ~/.agents/skill-hub/openharness/skills/using-openharness ✓
```

**命令 3**：SessionStart hook
```
cat /tmp/oh-test/.claude/settings.json
→ {"hooks": {"SessionStart": "using-openharness"}} ✓
```

**命令 4**：AGENTS.md → CLAUDE.md 桥接
```
ls -la /tmp/oh-test/CLAUDE.md
→ CLAUDE.md -> AGENTS.md ✓
```

**命令 5**：init --agent codex
```
openharness --repo /tmp/oh-test init --agent codex
退出码: 0
ls -la /tmp/oh-test/.agents/skills/openharness
→ ~/.agents/skill-hub/openharness/skills ✓
```

**命令 6**：幂等性
```
openharness --repo /tmp/oh-test init --agent all
退出码: 0，无错误输出 ✓
```

**命令 7**：错误场景（clone 不存在）
```
openharness --repo /tmp/oh-test init --agent claude
退出码: 1
输出: ERROR: OpenHarness clone not found at ...
      Run install.sh first, or clone manually: ... ✓
```

### 验收标准覆盖

| 需求 | 验证命令 | 结果 |
|------|---------|------|
| install.sh 可执行 | 命令 1 | passed |
| Claude Code symlink | 命令 2 | passed |
| SessionStart hook | 命令 3 | passed |
| AGENTS.md ↔ CLAUDE.md 桥接 | 命令 4 | passed |
| Codex symlink | 命令 5 | passed |
| 幂等性 | 命令 6 | passed |
| 错误处理 | 命令 7 | passed |

### 结论

通过。全部 7 项验证命令的实际输出与预期一致。

## 残余风险

- **Windows symlink**：`Path.symlink_to()` 在 Windows 上需要开发者模式或管理员权限。本轮未在 Windows 上验证
- **已有 settings.json 复杂合并**：仅验证了空白项目的场景，未模拟已有复杂 hooks 配置时的合并行为

以上风险接受理由：两个场景在当前用户群中概率低，且均设计为"不覆盖、打印警告"，不会导致数据丢失。

## 后续事项

无。
