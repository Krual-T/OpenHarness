# 验证策略

## 验证路径

- **计划路径**：在临时项目中运行 `init --agent codex`，检查 `.codex/hooks.json` 和 `.codex/config.toml` 的内容
- **回退路径**：无 Codex CLI 环境也可验证——文件内容是静态 JSON/TOML，`cat` 即可判断正确性

## 必需命令

### 1. 验证 hooks.json

```bash
cat /tmp/oh-test/.codex/hooks.json
```

期望退出码：0
期望：`hooks.SessionStart[0].matcher` 为 `"startup|resume"`，command 指向 SKILL.md

### 2. 验证 config.toml

```bash
cat /tmp/oh-test/.codex/config.toml
```

期望退出码：0
期望：包含 `codex_hooks = true`

### 3. 验证 config.toml 已存在时不覆盖

```bash
echo "# existing config" > /tmp/oh-test/.codex/config.toml
openharness --repo /tmp/oh-test init --agent codex
```

期望：打印警告，不修改已有 config.toml

## 预期结果

| 验证项 | 预期 |
|--------|------|
| hooks.json 存在且格式正确 | SessionStart hook，command 指向 SKILL.md |
| config.toml 新建场景 | 含 `codex_hooks = true` |
| config.toml 已存在场景 | 打印警告，不覆盖 |

## 可追溯性

| 需求 | 验证命令 |
|------|---------|
| hooks.json 创建 | 命令 1 |
| config.toml 创建 | 命令 2 |
| config.toml 不覆盖 | 命令 3 |

## 风险接受

- 不在真实 Codex CLI 环境测试 hook 触发——文件内容验证足够

## 验证执行计划

- 实现完成后立即在临时项目中执行
