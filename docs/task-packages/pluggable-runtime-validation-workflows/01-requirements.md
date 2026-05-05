# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Intent
本任务的意图是为 OpenHarness 探索一种可插拔的 runtime 级验证机制。

OpenHarness 当前承接 task package、skill-hub、流程治理和验证记录，但 runtime 级测试不是一个可以由通用框架单独完成的东西。每个项目的真实入口、外部系统、运行环境、账号凭证、观测面和失败判定都不同，因此 runtime 验证必须允许项目具体分析、具体接入。

这个任务希望让 OpenHarness 能表达和承接这类项目专属 runtime 工作流，而不是把 `pytest`、`lark-cli` 或任何单一工具误认为完整测试边界。

## Purpose
本包要回答的是 OpenHarness 自己的问题：

- OpenHarness 应如何理解 runtime 级验证与单元测试、集成测试、人工验收之间的关系。
- 项目专属 runtime 工作流应以 skill、脚本、CLI 扩展、adapter、配置约定，还是其他形式接入。
- OpenHarness 如何发现这些工作流。
- OpenHarness 如何把运行前置条件、执行过程、结果、证据和未覆盖缺口统一报告出来。
- OpenHarness 如何避免把某个具体工具的能力误抽象成通用机制。

## First Reference Example
`lark-cli` 相关工作流是第一个参考样例。

它的作用是帮助 OpenHarness 面对一个真实场景：某个项目的 runtime 验证依赖飞书或 Lark 的真实交互，以往需要人工客户端操作，现在可以尝试用命令行工具、脚本和项目观测面自动化其中一部分流程。

这个样例用于验证 OpenHarness 的接入机制是否现实，不用于把 `lark-cli` 提升为通用 runtime 测试模型。

## Relationship To Project-Specific Work
`../openrelay` 中的任务应负责描述 openrelay 自己的真实飞书 runtime 验证需求。

本任务负责从这类真实项目需求中抽象 OpenHarness 的通用承接方式。两边应保持分工：项目任务证明具体需要，OpenHarness 任务沉淀可复用机制。

## Non-Goals
- 不在本包里实现 openrelay 的具体飞书测试场景。
- 不把 runtime 验证简化成某个固定命令。
- 不要求所有项目都使用同一种工具或同一种外部系统。
- 不提前决定最终形态一定是 skill、CLI 子命令、adapter 目录或配置文件。
