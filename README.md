# Requirements Spec

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate Skill](https://github.com/messiwu/requirements-spec/actions/workflows/validate.yml/badge.svg)](https://github.com/messiwu/requirements-spec/actions/workflows/validate.yml)

[INFERRED] `requirements-spec` 是一个面向产品需求工作的 Agent Skill。它帮助 agent 将已有 PRD、零散描述和相互冲突的材料，整理成架构、开发和测试可以共同使用的需求基线。

[COMMON] 需求文档的核心质量标准不是篇幅或章节数量，而是下游无需替产品决定业务结果。这个 skill 会区分原始陈述、证据、推导、建议和已采纳决定，并把尚未闭合的问题留在明面上。

## 能做什么

- [INFERRED] 补全已有 PRD：定位逻辑漏洞、字段语义缺失、流程断点、规则冲突和不可判定的验收标准。
- [INFERRED] 从抽象描述开始：先明确用户任务、期望结果和本期范围，再逐步形成需求。
- [INFERRED] 评审需求：从架构、开发和测试的消费视角给出定位、反例、影响和最小修复。
- [INFERRED] 对齐多份材料：保留来源和版本，显式处理文档、原型、会议记录之间的冲突。
- [INFERRED] 管理需求变更：区分候选提案和已采纳变更，维护新旧版本及受影响范围。
- [INFERRED] 覆盖企业产品、消费者产品和 Agent 产品，并按实际业务机制增减分析深度。

## 工作结果

[INFERRED] skill 默认生成四种逻辑视图。简单需求可以合并成一份文件，复杂需求可以按业务能力拆分。

```text
docs/requirements/<需求主题>/
├── 00-交接索引.md
├── 01-需求规格.md
├── 02-依据与决策.md
└── 03-验收与追溯.md
```

| 视图 | 解决的问题 |
|---|---|
| 交接索引 | 当前版本、有效范围、阻塞项和不同角色的阅读入口 |
| 需求规格 | 用户任务、业务对象、流程、规则、状态、异常和质量要求 |
| 依据与决策 | 信息来自哪里，哪些是建议，哪些已被采纳，哪些仍待处理 |
| 验收与追溯 | 如何判断需求满足，以及原始要求和验收条件如何相互对应 |

## 安装

### Codex

[INFERRED] 在 Codex 中可以让内置的 skill 安装器从 GitHub 安装：

```text
$skill-installer install https://github.com/messiwu/requirements-spec
```

[COMMON] 安装新 skill 后，重新启动或新开 Codex 会话，确保技能目录被重新发现。

### 使用 skills CLI

```bash
npx skills add messiwu/requirements-spec -g -a codex -y
```

[INFERRED] 如果希望把 skill 随项目共享，去掉 `-g`，并按 CLI 的交互提示选择项目范围。

### 手动安装

```bash
git clone https://github.com/messiwu/requirements-spec.git
cp -R requirements-spec ~/.codex/skills/requirements-spec
```

[COMMON] Windows 或其他 agent 的技能目录可能不同，请使用对应工具的用户级或项目级 skills 目录。

## 快速开始

### 补全已有 PRD

```text
$requirements-spec 请补全 docs/产品需求.md。
找出会迫使架构、开发或测试猜业务结果的地方，形成可交接的需求文档。
```

### 只有一句需求

```text
$requirements-spec 我想做一个帮助客服更快处理客户邮件的助手。
先明确用户任务、候选范围和关键分歧，再形成当前信息支持的需求草案。
```

### 只做需求评审

```text
$requirements-spec 只评审 docs/requirements/订单取消.md，不修改原文。
请给出问题位置、竞争解释、业务影响、最小修复和阻塞范围。
```

### 处理需求变更

```text
$requirements-spec 当前有效需求在 docs/requirements/订单取消/。
新提案是“支付后不允许取消”。请分析新旧行为差异和影响范围；提案未采纳前保留现行基线。
```

## 实际工作方式

```mermaid
flowchart LR
    A[原始材料] --> B[识别任务与范围]
    B --> C[发现缺口与冲突]
    C --> D[核实事实与作出业务决定]
    D --> E[需求规格与验收]
    E --> F[下游消费审查]
    F --> G[按切片发布需求基线]
    F -->|发现业务歧义| C
```

[INFERRED] 你不需要先手工填写模板。提供原始材料、现行基线和已知权限即可；agent 会读取适用的工作规程和模板，并继续推进不依赖未决问题的部分。

[INFERRED] 更完整的交互步骤见[实际工作使用手册](references/06-实际工作使用手册.md)，设计边界见[设计依据与边界](references/01-设计依据与边界.md)。

## 设计原则

- [INFERRED] 业务结果明确，技术实现保留选择空间。
- [INFERRED] 原始要求、观察证据、推导、建议和决定分别记录。
- [INFERRED] 未决问题区分待核实、待选择和待验证。
- [INFERRED] 按业务切片判断是否需求就绪，避免一个问题阻塞无关范围。
- [INFERRED] 图表只在能减少歧义时使用，并与正文和验收保持一致。
- [INFERRED] 模板按实际风险伸缩，不用空栏目制造完整感。

## 仓库结构

```text
requirements-spec/
├── SKILL.md                   Agent 入口与路由
├── agents/openai.yaml         Codex 展示信息
├── references/                方法、模板、示例和使用手册
├── assets/                    可选的项目 AGENTS.md 片段
├── scripts/                   项目接入与仓库校验脚本
├── .github/                   CI、Issue 与 PR 模板
├── CONTRIBUTING.md            贡献指南
├── CODE_OF_CONDUCT.md         社区行为准则
├── SECURITY.md                安全问题报告方式
└── LICENSE                    MIT 许可证
```

## 验证

```bash
python3 scripts/validate_skill.py
```

[KNOWN] 该脚本检查 skill 必需文件、YAML frontmatter、内部 Markdown 链接、模板和项目接入脚本的幂等行为。GitHub Actions 会在提交和 Pull Request 上执行同一检查。

[COMMON] 静态检查只能证明仓库结构和引用关系有效，无法证明具体业务需求正确。真实项目仍需业务负责人和下游使用者评审。

## 兼容性

| 环境 | 状态 |
|---|---|
| Codex | [COMPUTED] 已完成安装、显式调用与项目接入演练 |
| Agent Skills 兼容工具 | [INFERRED] 目录结构遵循 `SKILL.md` 约定；尚未逐一完成行为验证 |
| 独立文档使用 | [KNOWN] `references/` 内保留完整方法、模板和示例 |

## 项目级接入

[INFERRED] 全局安装后，个人使用无需逐个项目初始化。如果团队希望把入口随仓库共享，可以调用：

```text
$requirements-spec 给当前项目接入这套需求方法，保留已有 AGENTS.md 规则。
```

[KNOWN] 接入脚本只管理带有 `requirements-spec` 标记的规则段，并保留其他内容。项目级规则片段不能替代完整 skill；其他机器仍需安装本仓库。

## 路线与边界

[INFERRED] 当前重点是需求发现、需求规格和规格评审。技术架构、实施计划、编码和完整测试设计由后续角色基于需求基线继续完成。

[KNOWN] 合成示例和静态演练记录不构成跨行业效果证明。希望改进方法时，请提供能够复现业务歧义、越权补充或验收失败的具体案例。

## 贡献

[INFERRED] 欢迎提交真实、可复现的需求失败案例、模板改进和使用反馈。开始前请阅读[贡献指南](CONTRIBUTING.md)和[行为准则](CODE_OF_CONDUCT.md)。安全相关问题请按[安全说明](SECURITY.md)处理。

## 参考

[KNOWN] 仓库结构和安装说明参考了 [Agent Skills 标准](https://agentskills.io)、[Anthropic Skills](https://github.com/anthropics/skills)、[OpenAI Skills](https://github.com/openai/skills) 和 [Vercel Labs skills CLI](https://github.com/vercel-labs/skills) 的公开资料。方法内容由本项目独立编写。

## 许可证

[KNOWN] 本项目采用 [MIT License](LICENSE)。

[RULES I BROKE]: 无。
