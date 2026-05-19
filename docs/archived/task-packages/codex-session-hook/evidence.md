# 证据

## 验证结果

- **verify_by**: qualitative
- **Result**: passed

## 变更文件

- `openharness_cli/commands/init_cmd.py` — 新增 `_setup_codex_hook()`，创建 `.codex/hooks.json` 和 `.codex/config.toml`

## 语义审核

审核对象：`init --agent codex` 输出的 `.codex/` 配置文件

```bash
# 命令1: hooks.json
cat /tmp/oh-test/.codex/hooks.json
# → SessionStart hook, matcher: "startup|resume", command 指向 SKILL.md ✓

# 命令2: config.toml 新建
cat /tmp/oh-test/.codex/config.toml
# → [features]\ncodex_hooks = true ✓

# 命令2: 幂等性
openharness --repo /tmp/oh-test init --agent codex
# → 退出码 0，无警告 ✓

# 命令3: config.toml 已存在不含 codex_hooks
echo "# old config" > /tmp/oh-test/.codex/config.toml
openharness --repo /tmp/oh-test init --agent codex
# → WARNING 提示添加 codex_hooks = true ✓
```

### 验收标准覆盖

| 需求 | 结果 |
|------|------|
| hooks.json 创建 | passed |
| config.toml 新建 | passed |
| config.toml 已存在不覆盖 | passed |

## 残余风险

- 未在真实 Codex CLI 环境验证 hook 触发——文件格式与官方文档一致，风险可接受

## 后续事项

无。
