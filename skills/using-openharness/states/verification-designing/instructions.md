# 验证策略设计

## 步骤

1. **读需求文档**：打开 `requirements.md`，确认必须交付的结果和验收标准
2. **确定验证方式**：根据 `task-info.yaml.verification.verify_by` 选择
{% if verify_by == "unit_test" %}
   - `unit_test` → 列出测试文件和测试命令
{% elif verify_by == "qualitative" %}
   - `qualitative` → 明确审核对象、审核标准和判定准则；审核需由子 Agent 和人类审阅者双轨执行，两方结论均需记录
{% elif verify_by == "rwp" %}
   - `rwp` → 选择或编写运行时工作流脚本
{% else %}
   - 当前未设置 verify_by，请先确认验证方式后再继续
{% endif %}
3. **写 `verification-design.md`**：参考模板 `skills/using-openharness/references/templates/task-package.verification-design.md`
   - `## 验证路径`：计划路径（怎么验证）和预期执行路径
   - `## 必需命令`：逐条列出验证命令（命令、期望退出码、期望输出）
   - `## 预期结果`：每项验收标准的预期结果
   - `## 可追溯性`：需求 → 验证的对应关系
   - `## 风险接受`：哪些风险本轮不覆盖，以及为什么可以接受
4. **自检 阶段结束检查**

## 验证策略确认停点

写完 `verification-design.md` 后，必须向用户展示：

- 验证命令清单（可复制粘贴执行的命令）
- 覆盖矩阵（每项验收标准 → 对应验证命令）
- 本轮不覆盖的风险和接受理由

获得用户确认后才可 transition。用户否定 → 修正验证策略。

[可选] 在设计阶段就跑一次验证命令确认能正确失败，提前暴露验证策略自身的 bug。

## 阶段结束检查

1. 每项 Required Outcome 是否都有对应的验证方法？
2. 验证命令是否具体到可以直接复制粘贴执行？
3. 是否有至少一个边界或错误场景的验证？
4. 是否明确了本轮不覆盖的风险和接受理由？

全部能回答 → `openharness task-package transition <task-name>|<task-id> verification_designed`

`verification_designed` 是 gate 状态，CLI 会自动推进到 `implementing` 并输出实现阶段指令。

## verify_by 选择约束

三种验证方式的选用不是"哪个方便用哪个"。以下是强制分流规则：

| verify_by | 强制条件 | 反例 |
|-----------|---------|------|
| `unit_test` | 输入输出可编程、无外部副作用、失败可自动判定 | 不能对"代码可读性"用 unit_test |
| `qualitative` | 验证对象是设计文档、API 契约、命名规范等语义产物；审核必须由子 Agent 和人类审阅者双轨执行 | 不能对"函数返回 42"用 qualitative |
| `rwp` | 需要端到端运行、跨进程交互、或依赖外部环境 | 不能对纯逻辑单元用 rwp（过重） |

如果 `task-info.yaml.verification.verify_by` 与上述规则冲突，**阻塞**——回到 `requirements.md` 重新确定 verify_by。

{% if verify_by == "rwp" %}
### RWP 选择与设计约束

当 verify_by == rwp 时：
- **优先复用**现有 RWP（`openharness rwp list` 查看）。不要为每一个任务写新工作流脚本
- **必须声明**运行环境依赖（Python 版本、系统包、网络条件）和清理行为（工作流结束后是否需要手动回收资源）
- **必须明确**退出码语义：0 通过 / 1 失败 / 其他 = 环境异常
- 工作流脚本的 stdout 和 stderr 不可混用——stdout 放结构化产物，stderr 放人类可读日志
- **预期结果必须可逐项比对**：verifying 阶段会由子 Agent 读取工作流输出（stdout/stderr/产物），对照 `## 预期结果` 逐项比对。预期结果不能写成"输出正常"或"运行成功"——必须写具体期望（退出码 0、stdout 包含某字段、产物文件存在且非空等），否则子 Agent 无法产出结构化发现
{% endif %}

## 失败回退

验证策略设计阶段如果卡住，不要强行推进：

| 卡住原因 | 回退动作 |
|---------|---------|
| 某项必须交付的结果找不到对应验证方法 | 回到 `requirements.md` 修正该结果——它不可验证，等于没写 |
| 验证命令无法精确到复制粘贴执行 | 命令依赖的上下文不完整——补充文件路径、参数、环境变量 |
| verify_by 与需求性质冲突 | 重新提议 verify_by 并更新 `task-info.yaml` |
| 无法决定边界场景的验证粒度 | 优先覆盖安全/数据完整性边界；UI 微调类边界可声明不覆盖 |

## 要点

- 验证策略是"契约先行"：实现代码时必须让这些验证通过
- 不要在这里写实现方案——那是 `overview-design.md` 和 `detailed-design.md` 的职责
- 如果发现验证策略本身有歧义，回到 `requirements.md` 澄清需求
- 模板位于 `skills/using-openharness/references/templates/task-package.verification-design.md`
- `## 必需命令` 中每条命令的期望退出码必须写明——implementing 和 verifying 阶段依赖这个来做 pass/fail 判定
- 你设计的每一条验证命令，implementing 阶段 agent 会在 Goal-Driven Execution 中逐条执行。确保命令可复制粘贴、退出码含义明确。verifying 阶段 agent 在此基础上做正确性判定——三个阶段形成闭环：设计验证 → 执行验证 → 判定验证

## 常见失败模式

- 把验证命令写成抽象描述（"运行测试"），而非可执行命令（`pytest tests/test_xxx.py -v`）
- verify_by == rwp 时没有检查现有 RWP 就新建工作流脚本，导致重复
- 对定性验证（qualitative）不写判定准则，只写"审查通过"，导致 verifying 阶段无判断标准
- 定性验证只安排了 AI 审核未安排人类审核——人类审阅者的反馈是定性审核的必要组成部分，缺失则审核不完整
- 对所有能想到的验证都塞进去，导致 implementing 阶段验证负担过重——只验证必须交付的结果，边界场景保留在 `## 风险接受`
- rwp 预期结果写成"运行成功""输出正常"等无法逐项比对的形式——verifying 阶段子 Agent 需要具体期望才能产出结构化发现，模糊预期导致双轨审核空转
