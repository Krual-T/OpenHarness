# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> 按 `task-info.yaml.verification.verify_by` 类型选择对应章节填写。不要求全部填写——只写实际执行的。

## Verification Result
- **verify_by**: <unit_test / qualitative / rwp>
- **Result**: <passed / failed>

## Test Results

`verify_by: unit_test` 时填写：

- 测试命令 + 结果（退出码、通过数/失败数）
- 变更文件清单
- 验收标准覆盖表

示例：
```
pytest tests/test_xxx.py -v
结果：3 passed, 0 failed

变更文件：
- path/to/file.py — 改动说明
- tests/test_xxx.py — 新增测试

验收标准覆盖：
| 标准 | 证据 |
|------|------|
| 某项标准 | test_xxx ✓ |
```

## Semantic Review

`verify_by: qualitative` 时填写：

- 审核对象（文件、文档、设计）
- 发现（问题、改进点）
- 结论
- 问题是否已闭合

## Runtime Observation

`verify_by: rwp` 时填写：

- 工作流名称
- 观察结果
- 产物路径
- 盲区说明

## Residual Risks
本轮未覆盖的风险、接受理由、触发重新审查的条件。

## Follow-ups
后续任务、剩余决策、延后事项。没有时写"无"。
