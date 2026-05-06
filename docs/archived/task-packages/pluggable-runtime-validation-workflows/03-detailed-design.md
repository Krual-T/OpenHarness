# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
主验证路径分两层。

第一层先锁住协议与 CLI 行为：

- `openharness` 顶层 parser 必须暴露 `rwp` 子命令。
- `openharness rwp list` 必须能从 `.harness/rwp/workflows/*/workflow.md` 读取摘要。
- `openharness rwp show <workflow>` 必须输出完整 `workflow.md`。
- `openharness rwp run <workflow> <script.py> [args...]` 必须显式执行 workflow 脚本。
- `openharness rwp run` 必须自动尝试加载 `.harness/.env` 和 `.harness/rwp/.env`。
- `from openharness.rwp import get_logger` 必须可用，且 `get_logger()` 不带参数。

第二层再锁住 task-package 写回和文档边界：

- `03-detailed-design.md` 要能写出某个 workflow 为什么被纳入验证计划。
- `04-verification.md` 要能写出实际执行命令、退出码、stdout/stderr 摘要和 runtime 观察结果。
- `05-evidence.md` 要能写出 artifact 路径、日志路径或其他证据索引。

测试顺序建议先从 parser 和协议读写开始，再到 runner 和 runtime API，最后才改文档引用。

## Files Added Or Changed
本轮实现落点应至少覆盖这些表面：

- `openharness_cli/cli.py`
  - 增加 `rwp` 子命令及其子命令树。
- `openharness_cli/commands.py`
  - 实现 `cmd_rwp` 相关逻辑。
- `openharness_cli/repository.py`
  - 增加 RWP 目录发现、workflow 文档读取和脚本路径解析。
- `openharness_cli/models.py`
  - 增加 RWP 相关数据模型。
- `openharness/rwp.py`
  - 提供 `get_logger()`。
- `tests/openharness_cases/*`
  - 锁住 parser、RWP 发现、run 行为、环境加载和 runtime API。
- `docs/archived/task-packages/pluggable-runtime-validation-workflows/*`
  - 同步 task package 的 02/03/04/05 文档与状态。

这些落点合理的原因是：CLI、repository、models 和 runtime API 分别承载解析、发现、数据形态和脚本侧调用点，测试则必须跟着这些契约一起变化。

## Interfaces
`openharness rwp` 的接口精度如下：

- `openharness rwp list`
  - 输出所有 workflow 的 `name`、`description` 和 pack 路径。
  - 只读，不执行脚本。
- `openharness rwp show <workflow>`
  - `<workflow>` 既可以是 workflow 名，也可以是目录名。
  - 输出完整 `workflow.md`。
- `openharness rwp run <workflow> <script.py> [args...]`
  - `<script.py>` 必须显式指定。
  - 只执行 `.harness/rwp/workflows/<workflow>/scripts/` 下的 `.py` 文件。
  - 执行方式固定为 `uv run python <script-path> [args...]`。
  - 先自动尝试加载 `.harness/.env` 和 `.harness/rwp/.env`，再执行脚本。
  - `args` 原样透传给脚本，不做语义解释。

`openharness.rwp` 的 runtime API 最小接口如下：

- `from openharness.rwp import get_logger`
- `get_logger()` 不带参数，返回标准 `logging.Logger`
- OpenHarness 不对 logger 的文件处理器、路径策略或命名规则做强约束

脚本侧契约如下：

- workflow 脚本放在 `scripts/` 下。
- 项目自有复用代码放在 `libs/` 下。
- workflow 脚本可以导入项目自有 `libs/`，也可以导入 `openharness.rwp`。
- OpenHarness 不直接执行 `libs/` 里的函数。

## Module Internals
内部职责建议拆成四块：

1. `RWP discovery`
   - 负责扫描 `.harness/rwp/workflows/`。
   - 负责读取 `workflow.md`。
   - 负责给 `list` 和 `show` 提供数据。
2. `RWP runner`
   - 负责校验 workflow 与脚本路径。
   - 负责拼接 `uv run python` 命令。
   - 负责加载 `.env` 并执行脚本。
3. `RWP runtime API`
   - 负责提供 `get_logger()`。
   - 负责让脚本用统一方式接入 OpenHarness runtime 上下文。
4. `task-package writeback`
   - 负责把选中的 workflow、执行结果、观察和证据写回 `03/04/05`。

`RWP runner` 和 `RWP runtime API` 的职责要分开：runner 负责“怎么跑”，API 负责“脚本里怎么拿到标准 logger”。这能避免 CLI 和脚本侧逻辑耦合在一起。

## Data Semantics
RWP 的关键数据语义如下：

- `workflow.md`
  - `name` 是 workflow 的稳定标识。
  - `description` 是 agent 做相关性判断的第一信号。
  - 正文解释用途、环境、脚本、观察点、成功标准、失败证据、限制和写回指导。
- `scripts/`
  - 目录内每个 `.py` 文件都是显式可运行脚本。
  - 脚本名就是调用入口名，不再额外注册。
- `.harness/.env` 与 `.harness/rwp/.env`
  - 两者都应在 `run` 时自动尝试加载。
  - 具体加载顺序以后者覆盖前者。
- `get_logger()`
  - 返回标准 `logging.Logger`。
  - 不强迫 workflow 采用统一落盘规则。

如果 workflow 需要统一日志位置，那是 workflow 自己通过 logger handler 或其他脚本机制完成，不是 OpenHarness CLI 的职责。

## Error Handling
主要失败路径如下：

- 找不到 `.harness/rwp/workflows/<workflow>/workflow.md`
  - `list` 应跳过或报告该条目无效。
  - `show` 和 `run` 应报清晰错误。
- `workflow.md` 缺少 `name` 或 `description`
  - 该 workflow 不应进入摘要列表。
  - 应报协议错误，提示 workflow 不完整。
- 脚本不存在或不在 `scripts/` 下
  - `run` 应直接失败，不回退到 `libs/` 或其他路径。
- `.env` 解析失败
  - `run` 应失败并报告哪个环境文件有问题。
- 脚本返回非零退出码
  - runner 应保留退出码，并把失败写回 task-package 验证记录。
- `get_logger()` 被脚本导入但 runtime context 不完整
  - 先按标准 logger 返回，避免把日志工具变成 runtime blocker。

静默出错风险主要有两个：

- workflow 被发现但没有进入 task package，导致 runtime 证据仍然游离在目录里。
- workflow 执行成功但没有写回 `04/05`，导致外部证据没有进入 task package 闭环。

这两个风险都必须在 `04-verification.md` 和 `05-evidence.md` 里显式检查。

## Migration Notes
迁移顺序建议如下：

1. 先新增 `openharness.rwp` runtime API。
2. 再实现 `openharness rwp` 子命令和 `.harness/rwp/workflows/` 发现。
3. 再接入 `.harness/.env` 与 `.harness/rwp/.env` 的加载。
4. 再更新 task package 文档与协议引用，把旧 helper 术语替换为 RWP。
5. 最后补充迁移或归档说明，确保旧 runtime helper 文档不再作为首要入口。

回滚触发点：

- `rwp` 子命令破坏现有顶层命令解析。
- `run` 不能稳定执行显式脚本。
- `get_logger()` 不能被脚本直接导入。
- 新旧文档同时保留但语义冲突，导致 agent 无法判断该看哪份。

## Stage Gates
进入实施前必须已经确定：

- RWP 目录位置是 `.harness/rwp/workflows/`。
- `run` 必须显式指定脚本名。
- `run` 只执行 `.py` 脚本。
- `run` 自动加载 `.harness/.env` 和 `.harness/rwp/.env`。
- `openharness.rwp.get_logger()` 是 OpenHarness 提供的唯一 runtime API 起点。
- `libs/` 只承载项目自有复用代码。
- `logs/` 只承载运行证据与观察结果。
- 旧 helper 术语已在 overview 里定性为重构目标，而不是并行体系。

## Decision Closure
已接受的挑战：

- 不再把 RWP 注册成 YAML。
- 不再让 CLI 自动选择 workflow。
- 不再预定义 `check-env`、`observe` 这类内部 action 名称。

已拒绝的挑战：

- 让 `run` 自动猜测脚本名。
- 让 `libs/` 成为可直接运行的 entry surface。
- 让 OpenHarness 统一接管 workflow 的日志落盘规则。

已延期的挑战：

- 旧 runtime helper 文档如何逐步迁移成 RWP 文档索引。
- 是否需要更丰富的 runtime context API，当前只先保留 `get_logger()`。

## Recommended Diagrams
建议补一张 `PlantUML` 时序图，表达：

- 主智能体派子智能体做 workflow 选择。
- 子智能体读取 `list/show`。
- 主智能体把选中的 RWP 纳入 `03`。
- runner 通过 `run` 执行脚本。
- 结果写回 `04/05`。

如果后续实现中还出现 env 加载或 logger 处理歧义，再补一张数据流图。

## Detailed Reflection
挑战一：`get_logger()` 是否要负责日志落盘？

结论：不负责。OpenHarness 只提供标准 logger 工厂，具体写到哪里由 workflow 自己决定。这样可以避免把日志路径策略和 runner 绑定死。

挑战二：`run` 是否要支持非 Python 脚本？

结论：本轮拒绝。第一版只支持 `.py`，理由是仓库整体已经要求 Python 命令统一用 `uv run ...`，而且这样最容易验证。

挑战三：`show` 是否必须接受目录名和 workflow 名两种输入？

结论：接受。这样能兼容目录名和元数据名不完全一致的情况，但两者都必须能唯一定位到一个 workflow。
