# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 为 parser 帮助输出新增自动化测试，断言顶层和关键子命令帮助页的关键文案。
  - 执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 确认 task package 协议仍成立。
- Fallback Path:
  - 如果当前环境不能直接调用安装后的 `openharness --help`，则至少通过 `build_parser().format_help()` 与子 parser `format_help()` 证明帮助页文本已生成；若两者都未验证，则不能宣称完成。
- Planned Evidence:
  - 帮助页相关测试。
  - 更新后的 CLI parser 文案。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/cli.py`：补充各命令 help/description/epilog。
- `skills/using-openharness/tests/openharness_cases/test_entrypoint.py`：增加帮助输出断言。
- 如需要，再补文档中对帮助使用方式的说明。

## Interfaces
对外接口不变，变化的是帮助文本质量。

## Stage Gates
- 先有失败测试，再补帮助文案。
- `update --help` 必须说明真实行为而不是只显示空参数页。

## Decision Closure
- 接受：继续使用 `argparse`。
- 拒绝：仅靠 README 承担帮助职责。

## Error Handling
- 帮助页必须避免误导，例如 `update` 要明确更新的是 OpenHarness 自身，而不是当前业务仓库。

## Migration Notes
- 无命令迁移，只是帮助质量提升。

## Detailed Reflection
帮助页也是接口的一部分，必须纳入测试；否则它会在功能迭代时自然退化。
