# 第一组：统一入口与需求澄清

状态：候选方案，待讨论确认。更新于 2026-11-16。

已确认前提：以 [mattpocock/skills](https://github.com/mattpocock/skills) 为基础补充自动化能力；面向 Codex 与 Claude Code；默认交付已验证、已独立审查的 PR，明确授权时可自动合并；首版覆盖用户启动的单项任务持续推进；完整 grilling 仅在明确要求深挖时启用。见[讨论记录](development-skills-session.md)与[词汇表](../../GLOSSARY.md)。

## 本组建议

统一开发入口已于 2026-11-17 由用户命名为 `octo-mode`；另有一个用户主动请求的深度设计入口，仍暂称 `design`。它们是本仓库补充的编排层：实现、诊断、TDD、审查等底层能力优先复用 Matt 的 skills，pstack 只提供路由与执行协议参考。常规澄清是开发入口的内部步骤；帮助内容是只读分支；领域建模是按需复用的方法。

入口应尽量由明确的仓库开发请求自动触发，也保留显式调用以便纠偏。`octo-mode` 初版已创建；两个目标宿主能否可靠自动触发、能否按要求衔接上游能力，仍需要继续评测。

本组的“废弃独立入口”表示新套件不再单独发布该命令，其有用行为可以进入共享方法；不要求删除或改写用户已安装的上游 skills。具体源文件迁移在整体设计确认后进行。

## 统一入口：逐项取舍

| 原能力 | 建议 | 保留内容 | 调整或移除内容 | 理由 |
| --- | --- | --- | --- | --- |
| Matt `implement` + `implement-spec` | 作为实现与质量闭环的基础，由统一入口按需衔接 | 单任务实现、TDD、依赖图、隔离执行、总审查与修复 | 让用户自行选择实现入口和手动推进后续阶段；具体 diff 范围、内部调用与宿主支持在后续组确认 | 新套件应增强 Matt 的现有执行能力，而不是先重写一套 worker |
| pstack `poteto-mode` | 仅借鉴路由思路，不作为移植基础 | 识别意图、任务选路、自动调用所需方法、推进到已授权终点 | 作者个人风格、Cursor API/模型默认、所有任务固定走同一组前后处理、仅显式 slash 的默认发现方式 | 路由思路可减少手动串流程；新入口仍以 Matt 的能力为执行基础，避免移植另一套平行体系 |
| Matt `ask-matt` + pstack `poteto-help` | 作为只读帮助知识来源；常规开发不再要求用户先经过选择器 | 解释能力、说明当前适合哪条路径、帮助请求保持只读 | 推荐一串命令再让用户重新发送和逐个调用的常规开发路径；本补充套件不新增平行帮助入口 | 统一入口负责选路；帮助仍有价值，可以作为同一入口的分支或按需参考，上游入口仍可独立使用 |
| pstack `in-your-own-words` | 借鉴并内嵌到任务接入，不移植独立入口 | 复杂或容易误解时，一句话说明目标与完成标准 | 每个小改动固定复述、复述后默认等待“你理解对了”的确认 | 一句话行为适合内嵌，无需增加一个入口或审批点 |
| pstack `sharpen` | 借鉴拆解方法并并入任务准备，不移植独立入口 | 第一手材料、适合的专业方法、能独立判断结果的验收证据 | 默认做一轮专家分析并重写 prompt，让用户再发送；对已有明确任务额外加深方法的固定仪式 | 当前目标是代理直接把工作做完整；提示词润色可以通过自然语言单独请求，不必占一个开发入口 |
| pstack `figure-it-out` | 借鉴为内部复杂任务分支 | 在没有合适流程时形成专用计划，优先解决未知，逐单元验证和记录决策 | 要用户记得何时另开此入口；在已明确的小任务里反复设计流程 | 支持自动选路的兜底；具体规划深度、预算和验证在后续组讨论 |
| Matt `wayfinder` | 首版不纳入通用入口，保留大型探索的参考材料 | 已决/待决/未知/范围外的区分，以及按依赖解决问题 | 一票一会话、以决策地图为主要交付、持续人工调度的默认工作方式 | 上游明确面向跨多会话的巨大模糊探索，产生决策而非交付；与首版单任务目标不完全重合。未来若需要项目级探索再讨论 |

来源：[implement][m-implement]、[implement-spec][m-implement-spec]、[poteto-mode][p-mode]、[ask-matt][m-ask]、[poteto-help][p-help]、[in-your-own-words][p-words]、[sharpen][p-sharpen]、[figure-it-out][p-figure]、[wayfinder][m-wayfinder]。原版事实与候选调整应分开理解；此表是取舍建议，未验证收益。

## 需求澄清：逐项取舍

| 原能力 | 建议 | 保留内容 | 调整或移除内容 | 理由 |
| --- | --- | --- | --- | --- |
| Matt `grilling` | 保留方法，分常规与深度两种使用方式 | 先查事实；真正的决定交给人；给推荐答案；按依赖组织问题 | 常规开发不要求穷尽设计树；便宜事实查询不强制起子代理；没有未知时不启动访谈 | 需要保留对齐能力，同时让工作量随不确定性变化；有复杂事实任务再委派 |
| Matt `grill-me` + `grill-with-docs` | 合并为一个深度设计入口 | 用户主动要求时系统性访谈；有仓库时按需记录有价值结论 | 仅因有没有工作目录而分两个命令；常规开发一律先走完整访谈 | 它们调用同一 grilling 方法，区别主要是持久化；文档策略可以随环境与结论决定 |
| Matt `domain-modeling` | 保留独立的共享方法，按需触发 | 发现术语冲突、业务概念或关系不清时澄清；确认后及时记 glossary；重要取舍才记 ADR | 把每次读取 glossary 当成建模；每个 bug 都要求词汇表和 ADR；流程状态混进 glossary | 它解决业务含义问题，可供设计、测试和审查复用，不适合全部塞进入口 |
| Matt `to-spec` | 本组将“澄清结果交给执行”合并到入口；完整规格能力留到规划组细化 | 问题、范围、验收、已定决策、必要验证方向可被后续执行读取 | 小任务必须长用户故事、发 tracker、手动调用；重问已经确认的信息 | 简单任务只需最小上下文，大任务才需要完整规格；减少重复确认与格式成本 |
| Matt/pstack `prototype` | 按需保留，作为调查和设计方法 | 用实际运行回答可观测问题，并把结果带回当前任务 | 每个技术分叉都做原型；仅为阶段切换要求用户人工 handoff | 源码读取、现有测试或小 probe 已能回答时，用更便宜方式；完整原型取舍后续单独讨论 |
| Matt `to-questionnaire` | 按需保留为外部信息采集工具，不进入常规开发链 | 知识在第三方且当前工具无法获取时，整理可独立作答的问题 | 为普通需求多加一轮“问卷的访谈”；默认要求用户给每个实现决定答卷 | 解决的是第三方知识缺口，和当前用户澄清是不同任务 |
| Matt `research` / pstack `how`、`why` | 本组保留“问题能自己查就自己查”的接口，内部组合留后续组 | 读当前实现、历史与一手资料，区分观察、推断、未知 | 无证据猜测；把可查事实交给用户；每个便宜查询都生成独立长研究文件 | 它们是澄清的事实支撑，不必成为人手动选择的前置命令 |

来源：[grilling][m-grilling]、[grill-me][m-grill-me]、[grill-with-docs][m-grill-docs]、[domain-modeling][m-domain]、[to-spec][m-spec]、[Matt prototype][m-prototype]、[pstack prototype][p-prototype]、[to-questionnaire][m-questionnaire]、[research][m-research]、[how][p-how]、[why][p-why]。

## 统一入口的最小职责

1. **识别当前意图。** 咨询、只读调查、设计、审查和实现各走对应路径；讨论方案的请求保持设计，明确实施请求才进入实施。延续当前任务还是新任务也要判断。
2. **补齐事实。** 读取已有需求、相关代码、项目约定、现有验证方式及已确认决定。按问题需要读取，避免每个任务扫全仓或重建全部历史。
3. **形成最小任务简报。** 工作目标、验收条件、范围、需要保留的决定/假设和交付终点；引用已有规格，不重新抄写。这是候选产物，尚未确定名称与落盘格式。
4. **只问阻塞决定。** 仅当前信息无法确定的产品/验收决定、不可逆取舍需要人答；普通技术实现由代理结合仓库证据选择。以一轮当前独立且真正阻塞的问题为单位，给推荐与影响；已回答的不重复问。后来出现新的关键冲突可以再问。
5. **自动衔接与执行。** 在原请求已经授权实施且必要决定解决后，自动进入相应实现、验证、审查、修复与交付阶段；帮助或纯设计请求不会因此自动升级为实施。各阶段详细职责在后续组细化。

重点是把“用户选择哪一个 skill”变成内部路由，同时让“用户决定要做成什么”仍可被清晰表达。

## 澄清策略与完成边界

| 问题类型 | 处理方式 | 示例 |
| --- | --- | --- |
| 当前实现的事实 | 查代码、配置、历史或运行结果 | 当前登录失败时是否会重试 |
| 能用实验解决的技术选择 | 选最便宜且足以判断的方法，比较结果后选择 | 两种索引哪种在目标查询上更合适 |
| 可逆的实现决定 | 尊重项目惯例，自行选择；重要假设可简记 | 内部 helper 如何拆分、现有命令足够时怎样验证 |
| 缺失且影响验收的产品/业务决定 | 给出推荐与取舍，向用户询问 | 订单超时到底关闭还是允许恢复 |
| 已由项目约定或用户回答解决的决定 | 直接沿用；发现冲突才重新提问 | 已明确每买家互不影响，再讨论并发实现时不重问 |
| 确需用户信息但尚未得到回答 | 继续可独立完成的工作；记录受影响部分与精确问题；需要时以待决定状态交接 | 接口文档不可达且默认行为会改变业务含义 |

一次任务进入实现的澄清完成条件：目标和可观察验收足够明确，范围与交付终点已知，受影响工作不存在未解决的产品/验收决定或不可逆取舍。无需把所有未来设计分支都想完；技术未知可以成为后续执行计划中的调查步骤。

普通任务不机械规定“最多问 N 个问题”。先减少能自己查的问题，再减少没有实际影响的分叉；不能为了满足轮数上限，把缺失的业务决定当成已获同意。无人值守不意味着无限等待用户，也不意味着替用户虚构答案。

深度设计时可使用设计树、反例和分轮提问，但沿用已决信息；“每个分支都曾访问”的形式目标不应制造与当前目标无关的问题。深度设计完成时应能给出可供用户判断的方案与剩余问题，而不是强制转入新一轮 prompt 改写、规格、拆票访谈。

## 文档产物按需生成

- 小改动：简报可留在当前任务上下文或既有任务记录，不要求独立 spec、完整 glossary 或 ADR。
- 已有规格：直接引用并补充本次已确认差异，避免第二份真相来源。
- 复杂工作或多人/多代理接力：把关键简报与决定落盘，便于后续执行和核验；具体文件格式在规划/运行状态组决定。
- 新领域术语已确认：立即更新 glossary，保持纯词义。
- 架构决策确实难逆转、无背景难理解且经过真实取舍：记录 ADR。

按需文档不取消无人值守执行中的必要证据、进度和交接记录；这些由后续运行状态与验证组定义。这里仅决定需求澄清不必为每项小修改生产完整文档包。

## 场景对照

| 请求 | 原流程可能出现的成本 | 候选入口行为 |
| --- | --- | --- |
| “分页跳到下一页时重复显示最后一条，帮我修” | 用户先选诊断/实现/TDD/review 的组合 | 自动走缺陷路径，查实现和复现，修复验证；问题明确时无 grilling |
| “加退款申请” | 先完整访谈，再手动转 spec/tickets/implement | 查已有订单模型和规则；只问真正缺失的退款政策，答案已有则直接沿用；技术步骤由内部串联 |
| “先讨论退款政策，别改代码” | 若入口仅按关键词匹配可能误走实现 | 只设计和澄清，完成后给方案 |
| “深度推敲一下多租户权限设计” | 多个访谈入口可选，需要判断哪个会写文档 | 单一深度设计入口，按需建模、研究与原型；关键结论一次沉淀 |
| “这个权限模块怎么工作” | 全量工程规则可能过重 | 只读解释，达到回答目标即结束 |

上述是预期行为示例，未进行自动触发、耗时或结果质量测试。

## 本组待确认

- **Q6，入口触发：** 明确的仓库开发请求自动进入统一入口，显式调用作为快捷和纠偏方式；咨询、设计、审查按原意保持对应路径。建议采用。
- **Q7，澄清产物：** 按规模引用或记录一份最小任务简报；有新术语、重要取舍或复杂工作时才扩展文档。建议采用。

用户可以逐项修改表中取舍，本组候选不代表已删除任何现有能力。具体公开名称、skill 文件边界、触发元数据和宿主调用方式留到职责确认后再定。

## 固定源码来源

沿用首轮调研快照，未将 upstream main 的后续变化混入本轮建议。

[p-mode]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/poteto-mode/SKILL.md
[p-help]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/poteto-help/SKILL.md
[p-words]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/in-your-own-words/SKILL.md
[p-sharpen]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/sharpen/SKILL.md
[p-figure]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/figure-it-out/SKILL.md
[p-prototype]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/poteto-mode/playbooks/prototype.md
[p-how]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/how/SKILL.md
[p-why]: https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/why/SKILL.md
[m-implement]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/implement/SKILL.md
[m-implement-spec]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/implement-spec/SKILL.md
[m-ask]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/ask-matt/SKILL.md
[m-wayfinder]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/wayfinder/SKILL.md
[m-grilling]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/grilling/SKILL.md
[m-grill-me]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/grill-me/SKILL.md
[m-grill-docs]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/grill-with-docs/SKILL.md
[m-domain]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/domain-modeling/SKILL.md
[m-spec]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/to-spec/SKILL.md
[m-prototype]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/prototype/SKILL.md
[m-questionnaire]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/to-questionnaire/SKILL.md
[m-research]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/research/SKILL.md
