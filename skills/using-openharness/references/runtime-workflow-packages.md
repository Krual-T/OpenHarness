# Runtime Workflow Packages

Runtime Workflow Packages（RWP）是项目级运行时验证记录，由 OpenHarness CLI 发现和执行。

RWP 不是 Codex skill，不使用 `SKILL.md`。OpenHarness 通过渐进式披露控制上下文加载。

## Package Shape

```
.harness/rwp/
  rwplib/                     ← 所有 workflow 脚本共享的工具库（也兼容旧名 libs/）
    __init__.py
    ...
  logs/                       ← 运行时日志和观测产物
  workflows/
    <workflow-name>/
      workflow.md             ← workflow 定义（唯一入口）
      scripts/                ← 可执行脚本
        <script>.py
```

- `.harness/rwp/workflows` — 可发现 workflow 的根目录
- `workflows/<name>/` — 每个 workflow 一个目录，`workflow.md` 是唯一入口
- `rwplib/`（也兼容旧名 `libs/`）— Python 包，`openharness rwp run` 自动将其加入 `PYTHONPATH`，脚本可直接 `import rwplib` 或 `from rwplib.xxx import yyy`。项目自有复用代码放在此目录
- `logs/` — 运行时产物统一输出目录。运行时日志和观测产物写入此目录

`workflow.md` 以 metadata header 开头：

```markdown
---
name: <RWP_NAME>
description: <DESCRIPTION>
---
```

正文应覆盖：purpose、when to use、prerequisites、scripts/、runtime observation、success criteria、failure evidence、limitations、writeback guidance。

## Selection Flow

当任务可能需要运行时验证时，主 agent 应指派 subagent 选择候选 RWP：

1. 运行 `openharness rwp list`
2. 根据 `description` 筛选强候选
3. 只对有把握的候选运行 `openharness rwp view <workflow>`
4. 报告选定的 RWP、拒绝的近似匹配和写回点
5. 主 agent 在任务包中记录最终选择

OpenHarness CLI 不会自动选择 workflow。

## 创建新的 RWP

### 1. 使用 CLI 创建

```bash
openharness rwp create <workflow-name> "<description>"
```

这会自动创建目录结构并生成 `workflow.md`（含 name 和 description 的 metadata header）。

创建后编辑 `workflow.md` 补全各节内容。

### 2. 放脚本

将 Python 脚本放入 `scripts/` 目录。脚本只能在此目录下，不能嵌套子目录。文件名必须以 `.py` 结尾。OpenHarness does not define workflow-specific script names。

### 3. 加共享代码（可选）

如果多个脚本或 workflow 需要复用代码，放到 `.harness/rwp/rwplib/` 下。`openharness rwp run` 已将 `.harness/rwp/` 加入 `PYTHONPATH`，脚本中直接导入：

```python
from rwplib.auth import get_token
from rwplib.helpers import retry
```

### 4. 验证

```bash
openharness rwp list              # 确认出现在列表中
openharness rwp view <workflow>  # 确认内容
openharness rwp run <workflow> <script.py>   # 执行验证
```

## 脚本编写规范

### import 可用范围

`openharness rwp run` 执行脚本时，以下路径已加入 `PYTHONPATH`：

1. repo 根目录 — 可 `from openharness.rwp import get_logger`
2. `.harness/rwp/` — 可 `from rwplib.xxx import yyy`

### 日志与 Logger

`openharness rwp run` 自动尝试加载：

- `.harness/.env`
- `.harness/rwp/.env`

`.harness/rwp/.env` 中的值覆盖 `.harness/.env` 的值（规划中，当前未实现）。

workflow 脚本也可在 `workflow.md` 的 Prerequisites 节声明所需环境变量，由调用方在执行前设置。

OpenHarness 提供以下运行时 API：

```python
from openharness.rwp import get_logger

logger = get_logger()
```

`get_logger()` 返回标准 Python `logging.Logger`（name=`openharness.rwp`）。OpenHarness 不强制日志格式，每个 workflow 自行决定 handler 和输出方式。

### 产物路径

运行时产物统一写入 `.harness/rwp/logs/`：

```python
from pathlib import Path
import os

logs_dir = Path(os.environ.get("RWP_LOGS_DIR", ".harness/rwp/logs"))
output = logs_dir / "result.json"
output.write_text(...)
```

### 参数传递

```bash
openharness rwp run <workflow> <script.py> --target sandbox --verbose
```

`--target sandbox --verbose` 直接转发给脚本，OpenHarness 不做解释。

### 退出码

- `0` — 成功
- 非 `0` — 失败，CLI 会透传退出码

## Execution

```bash
openharness rwp run <workflow> <script.py> [args...]
```

约束：

- 脚本名必须显式指定
- 只允许 `scripts/` 下的 `.py` 文件
- 参数透传，不做解析
- 脚本名不能包含 `/` 或 `\`
- OpenHarness does not define workflow-specific script names

## 写回任务包

RWP 的使用必须写入任务包的正常流程：

- `overview-design.md` — 记录是否考虑 RWP、选定/拒绝/推迟了哪个
- `detailed-design.md` — 记录选定的 RWP、前置条件、脚本、预期观察、降级路径
- `plan.md` — 记录计划执行的命令、预期结果、偏差处理和阻塞回退
- `evidence.md` — 记录产物路径、日志路径、外部记录、人工步骤、残余风险、后续

如果没有匹配的 RWP，记录缺失而不是假装有运行时覆盖。
