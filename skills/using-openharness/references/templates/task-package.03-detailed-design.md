# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 用中文列出将执行的验证路径，命令本身保持英文原样。
- Fallback Path:
- 用中文说明如果主验证路径被阻塞时如何处理，以及何时不能宣称完成。
- Planned Evidence:
- 用中文写明预计要产出的证据、产物或观察结果。

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- 用中文列出将新增或修改的文件，并说明它们为什么在这轮需要变化。

## Interfaces
用中文写清楚这轮改动暴露或依赖的接口、契约和稳定边界。

## Error Handling
用中文说明失败路径、误用风险、校验边界和如何避免静默出错。

## Migration Notes
用中文描述迁移顺序、兼容策略、落地阶段和回滚注意事项。

## Detailed Reflection
用中文记录对测试策略、接口边界、迁移假设和验证路径的反思。
