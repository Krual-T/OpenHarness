# 验证策略

## 验证路径

- **计划路径**：在临时项目中执行安装 → 检查 symlink 和 settings.json → 验证桥接 → 重复运行确认幂等 → 检查 AGENTS.md bridging
- **回退路径**：如无 Claude Code 环境，跳过 SessionStart hook 的运行时验证，仅验证 JSON 文件内容正确
- **路径说明**：定性验证，判定标准为文件存在性、symlink 目标正确性和 JSON 内容匹配。不依赖外部服务

## 必需命令

### 1. 验证 install.sh + init --agent claude

```bash
# 准备临时项目
mkdir -p /tmp/oh-test-claude
echo "# Test Project" > /tmp/oh-test-claude/AGENTS.md
# 运行安装
./install.sh /tmp/oh-test-claude
```

期望退出码：0

### 2. 验证 Claude Code symlink

```bash
ls -la /tmp/oh-test-claude/.claude/skills/using-openharness
```

期望：symlink 指向 `~/.agents/skill-hub/openharness/skills/using-openharness`

### 3. 验证 SessionStart hook

```bash
cat /tmp/oh-test-claude/.claude/settings.json
```

期望：包含 `"hooks": {"SessionStart": "using-openharness"}`

### 4. 验证 AGENTS.md → CLAUDE.md 桥接

```bash
ls -la /tmp/oh-test-claude/CLAUDE.md
```

期望：symlink 指向 `AGENTS.md`

### 5. 验证 init --agent codex

```bash
openharness init --agent codex --repo /tmp/oh-test-claude
ls -la /tmp/oh-test-claude/.agents/skills/openharness
```

期望退出码：0，symlink 指向 `~/.agents/skill-hub/openharness/skills`

### 6. 验证幂等性

```bash
./install.sh /tmp/oh-test-claude
openharness init --agent all --repo /tmp/oh-test-claude
```

期望退出码：0，无错误输出

### 7. 验证错误场景：clone 不存在

```bash
mv ~/.agents/skill-hub/openharness ~/.agents/skill-hub/openharness.bak
openharness init --agent claude --repo /tmp/oh-test-claude
mv ~/.agents/skill-hub/openharness.bak ~/.agents/skill-hub/openharness
```

期望退出码：1，输出包含 "未找到"

### 8. 清理

```bash
rm -rf /tmp/oh-test-claude
```

## 预期结果

| 验证项 | 预期 |
|--------|------|
| install.sh 退出码 | 0 |
| Claude symlink 目标 | `~/.agents/skill-hub/openharness/skills/using-openharness` |
| settings.json 内容 | `"SessionStart": "using-openharness"` |
| CLAUDE.md 桥接 | symlink → AGENTS.md |
| Codex symlink 目标 | `~/.agents/skill-hub/openharness/skills` |
| 幂等运行退出码 | 0，stdout 无 ERROR |
| clone 不存在错误 | 退出码 1，stderr 含提示信息 |

## 可追溯性

| 需求 | 验证命令 |
|------|---------|
| install.sh 可执行 | 命令 1 |
| Claude Code symlink | 命令 2 |
| SessionStart hook | 命令 3 |
| AGENTS.md ↔ CLAUDE.md 桥接 | 命令 4 |
| Codex symlink | 命令 5 |
| 幂等性 | 命令 6 |
| 错误处理 | 命令 7 |

## 风险接受

- **Windows 兼容性**：本轮不验证。install.sh 依赖 bash 和 symlink，Windows 需 Git Bash 或 WSL
- **已有 settings.json 合并**：不模拟复杂 JSON 合并场景。合并逻辑在 detailed-design.md 中已精确描述，实现审查即可
- **网络故障**：clone 失败场景依赖网络环境，不在验证中模拟断网

## 验证执行计划

- 执行时机：implementing 阶段完成后立即执行
- 执行环境：Linux，git 和 uv 已安装
- 责任人：实施者
- 验证失败时：检查错误输出，回到 implementing 修复代码
