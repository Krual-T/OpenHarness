# 验证策略

## 验证路径

- **计划路径**：在临时 Git 目录中执行 `openharness init --agent claude`，检查所有预期目录和文件是否存在；再次执行 `init` 验证幂等性。
- **回退路径**：如果 CLI 不可用，直接审查 `init_cmd.py` 代码 — 确认所有 `mkdir` 调用都有 `exist_ok=True`，所有文件写入都有 `exists()` 保护。
- **路径说明**：计划路径是端到端验证，覆盖实际 CLI 行为。如果 CLI 未安装则回退到代码审查。

## 必需命令

```bash
# 1. 创建临时目录并执行 init
tmpdir=$(mktemp -d)
cd "$tmpdir"
git init
openharness init --agent claude

# 2. 验证目录和文件存在 (期望全部 PASS)
test -d .harness/rwp/rwplib && echo "PASS: .harness/rwp/rwplib/" || echo "FAIL: .harness/rwp/rwplib/"
test -f .harness/rwp/rwplib/__init__.py && echo "PASS: __init__.py" || echo "FAIL: __init__.py"
test -d .harness/rwp/workflows && echo "PASS: .harness/rwp/workflows/" || echo "FAIL: .harness/rwp/workflows/"
test -d .harness/locks && echo "PASS: .harness/locks/" || echo "FAIL: .harness/locks/"
test -d docs/task-packages && echo "PASS: docs/task-packages/" || echo "FAIL: docs/task-packages/"
test -d docs/archived/task-packages && echo "PASS: docs/archived/task-packages/" || echo "FAIL: docs/archived/task-packages/"

# 3. 验证幂等性 (期望退出码 0)
openharness init --agent claude
echo "exit code: $?"

# 4. 清理
rm -rf "$tmpdir"
```

期望退出码：全部为 0；幂等执行退出码也为 0。

## 预期结果

| 检查项 | 预期 |
|--------|------|
| `.harness/rwp/rwplib/__init__.py` | 空文件存在 |
| `.harness/rwp/workflows/` | 空目录存在 |
| `.harness/locks/` | 空目录存在 |
| `docs/task-packages/` | 空目录存在 |
| `docs/archived/task-packages/` | 空目录存在 |
| 幂等性 | 重复执行 `init` 退出码 0，不打印 ERROR |

## 可追溯性

| 需求 | 验证 |
|------|------|
| 交付结果 1: rwplib/__init__.py | `test -f .harness/rwp/rwplib/__init__.py` |
| 交付结果 2: workflows/ | `test -d .harness/rwp/workflows` |
| 交付结果 3: locks/ | `test -d .harness/locks` |
| 交付结果 4: docs/task-packages/ | `test -d docs/task-packages` |
| 交付结果 5: docs/archived/task-packages/ | `test -d docs/archived/task-packages` |
| 交付结果 6: 幂等性 | 再次执行 `init` 退出码为 0 |

全部覆盖，无缺口。

## 风险接受

- `.harness/settings.yaml` 不在项目级创建：该文件属于 OpenHarness 全局配置（`~/.agents/skill-hub/openharness/.harness/settings.yaml`），由 `update --set-default-mode` 管理。本轮不涉及全局配置初始化，接受此风险。

## 验证执行计划

- 执行时机：实现完成后立即执行
- 执行者：Shaokun.Tang
- 执行环境：任意 Linux 环境，需已安装 `openharness` CLI
- 验证失败时：回到 `implementing` 修改 `init_cmd.py`
