# Matt Pocock skills 完整盘点与无人值守适配判断

研究日期：2026-11-15。目标：先理解每项技能及现有本地安装，再判断如何为“高质量代码、减少人工串流程、可无人值守执行”组合它们。本报告没有安装或改写技能，也没有执行上游脚本、hook、工作流或示例中的命令。

## 版本、来源与调查边界

- 仓库：[`mattpocock/skills` 固定快照][repo-tree]，实际 clone 的 `HEAD` 为 **`5863806dd4e15c63174bee4e7515a4256792ecfa`**。
- 此提交的作者/提交时间都是 **2026-11-12 08:42:38 UTC**；标题是 `Merge pull request #1416 from mattpocock/software-factory-task-wording`。[提交记录][commit]
- [`package.json`][package] 和 [plugin manifest][manifest] 的版本都是 **1.3.2**。这是仓库/plugin 版本，不代表用户本地有同一版本号的 plugin。
- 先用浏览工具打开用户指定的 GitHub URL，再 shallow clone 到 `/private/tmp/mattpocock-skills-20261115-research`；以 clone 的实际 SHA 固定全文来源。逐项完整阅读全仓 **39 个 `SKILL.md`**，补读发布规则、调用规则、关键参考模板和 `software-factory` 的全部 5 篇支撑文档。
- 本地只读核对 [skills-lock.json](/Users/nonlinearthink/Documents/Projects/nonlinearthink/skills/skills-lock.json) 与 [.agents/skills](/Users/nonlinearthink/Documents/Projects/nonlinearthink/skills/.agents/skills)。本地 lock 的 SHA-256 为 `2d408f80db0ffd49956963883cf9bc26371233918f40df0ac89ab41299ed4895`，便于以后识别本次所见快照。
- 下文“用途、交互、依赖”是源码事实；“适配、保留/合并/按需/不采纳”是面向本次目标的**初步判断，均待决**。没有进行宿主调用兼容性、无人值守成功率、成本或恢复能力的运行测试。

## 先说关键发现

1. **本地并没有整体落后。** 本地 lock 的 38 项全部来自 Matt；这 38 个技能目录内的 **103 个文件**与当前上游对应目录逐字节一致。当前上游只多了尚未安装的 beta `software-factory`。没有本地独有技能，也没有已安装技能的行为版本差异。
2. **人工串流程是上游的一部分设计。** 正式发布的 27 项中，16 项是 user-invoked，11 项可由模型自动使用。上游明确把选择这些入口的认知成本留给人；`ask-matt` 负责推荐，不能自行串调其他 user-invoked 技能。[调用规则][invocation]、[skill mechanics][mechanics]
3. **已经存在自动化相关能力。** `implement-spec` 能按依赖图并发实现整份 spec，`chief-of-staff` 协调长期目标，`claude-handoff` 启动新后台 Claude，`loop-me` 设计可自动运行的 workflow，`software-factory` 设计事件驱动工厂。不能把体验问题简单归因为“Matt 没有自动化”。但它们分别是提示词编排、宿主 CLI 桥接或设计语言，不能合并解释成现成的持久任务系统。[implement-spec][skill-implement-spec]、[chief-of-staff][skill-chief-of-staff]、[claude-handoff][skill-claude-handoff]、[loop-me][skill-loop-me]、[software-factory][skill-software-factory]
4. **更合理的取舍单位是职责。** 质量纪律可保留；访谈与产品决定集中在运行前；任务状态、并发占用、重试上限、恢复和调度交给可验证的编排层。后半句是本报告的架构判断，不能仅凭安装任何一个 skill 宣称已实现。

## 数量与发布状态

以隐藏目录也在内的文件枚举为准，不只读 README。

| 类型/目录 | `SKILL.md` 数 | user-invoked | model-invoked | 正式 plugin 发布 | 本地安装 |
| --- | ---: | ---: | ---: | --- | ---: |
| `skills/engineering/`，日常工程 | 20 | 11 | 9 | 是 | 20 |
| `skills/productivity/`，日常生产力 | 7 | 5 | 2 | 是 | 7 |
| `skills/misc/`，冷冻的专用工具 | 4 | 0 | 4 | 否 | 4 |
| `skills/in-progress/`，公开 beta | 8 | 8 | 0 | 否 | 7 |
| `skills/deprecated/` | 0 | 0 | 0 | 否 | 0 |
| `.agents/` 等内部维护位置 | 0 | 0 | 0 | 不适用 | 不适用 |
| **全部** | **39** | **24** | **15** | **27 项** | **38** |

正式集合准确地等于 engineering + productivity，且 manifest 的 `skills` 数组为 27 项；misc、beta 不在其中。`misc` 明确 frozen/unmaintained；beta 可以改变或消失。内部 `.agents/` 有调用规范、写 docs 规范、安装块和 ADR，但没有额外 `SKILL.md`，不应当作技能计数。`in-progress/README.md` 只列 7 项，漏列了实际存在的 `chief-of-staff`，因此按 README 盘点会少算一个。[仓库规则][repo-agents]、[manifest][manifest]、[SCOPE][scope]、[misc 冷冻政策][frozen]、[beta README][beta-readme]

标记：**U** 表示源码意图为“用户调用”；**M** 表示“模型或用户都可调用”。U/M 反映 frontmatter 和配套 YAML 的设计，不是本次对各宿主强制效果的实测。`software-factory` 是唯一没有 `agents/openai.yaml` 的技能；它有 `disable-model-invocation: true`，但缺少其余 U 技能具有的 Codex `allow_implicit_invocation: false` 配对文件。[调用规范][invocation]、[software-factory 文件树][factory-tree]

## 全部技能逐项说明

每行技能名都链接到固定 SHA 的完整 `SKILL.md`。适配栏的“高/中/低”是定性判断：高是任务与权限已齐后可主要由代理执行；中是需一次前置选择或宿主适配；低是设计上要求人持续参与。它们不表示实测可靠性。

### 工程：20 项，正式发布

| 技能 | 用途与触发场景 | 主要输出 | 交互、依赖与副作用 | 无人值守适配与初步取舍（待决） |
| --- | --- | --- | --- | --- |
| [ask-matt][skill-ask-matt] · U | 不记得该用哪个技能时，解释 idea→ship 主流程、bug/triage/大项目入口以及上下文切换。 | 路由建议与流程解释。 | 推荐前必须读目标技能全文；它本身只指路，不替用户启动其他 U 技能；依赖人选择下一步。 | **低**。保留作帮助入口；不要把它当自动调度器。可把常用路径合并进更少的操作入口。 |
| [grill-with-docs][skill-grill-with-docs] · U | 在有工作目录的设计/计划讨论中反复访谈并沉淀领域语言。 | 共同理解、`GLOSSARY.md`，以及符合条件的 ADR。 | 同时调用 `grilling`、`domain-modeling`；连续等待人的决定；有文档写入。 | **低**。按需，用于不确定性高的需求；不宜每次小改都强制启动。 |
| [triage][skill-triage] · U | 外部原始 issue，或配置允许时的外部 PR，需要判断、复现、归类与补充。 | 分类/状态标签、agent brief、needs-info 记录；拒绝增强时的 `.out-of-scope/` 记录。 | 依赖 tracker 和标签映射；推荐后等维护者方向；必要时 grilling/domain-modeling；可发评论、改标签、关 issue。自动生成内容带 AI 声明。 | **中/低**。保留状态与 brief 结构；常规事实核验可自动做，范围决定及冲突状态须单独设计。不是实现前的必经站，`to-tickets` 产物已 ready。 |
| [improve-codebase-architecture][skill-improve-codebase-architecture] · U | 想寻找深模块机会，尤其最近频繁变化、难理解或难测试的区域。 | 临时目录中的自包含 HTML 候选报告，含 before/after 图、强度与首选建议。 | 读 glossary/ADR、调用 codebase-design、派 fresh subagent 探索；用 open/xdg-open/start 展示；人选候选后进入 grilling。HTML 引用 Tailwind/Mermaid CDN。 | 扫描 **高**、选型 **低**。按需；可自动产候选，实施前集中决策，避免无人值守到处重构。 |
| [setup-matt-pocock-skills][skill-setup-matt-pocock-skills] · U | 每个仓库首次配置 tracker、triage 标签与领域文档布局。 | `docs/agents/{issue-tracker,domain,triage-labels}.md`，已有 AGENTS/CLAUDE 中的导航块，缺失的 tracker 标签。 | 明说是 prompt-driven 而非确定脚本；探索后逐节确认并给写入草稿。支持 GitHub/`gh`、GitLab/`glab`、本地 Markdown、用户描述的其他 tracker；远端需可达。 | **低**，但只应做一次。保留/合并为仓库接入流程，配置应复用而非任务中重复询问。 |
| [to-spec][skill-to-spec] · U | 已讨论清楚，要把现有对话转成可实现 spec。 | 发布至 tracker 的 spec，含问题、方案、长用户故事、实现决定、测试决定、范围，标 `ready-for-agent`。 | 明确不再采访，但仍要向用户核对测试 seams；依赖 tracker/标签，读 glossary/ADR。避免容易过期的具体路径/代码，保留少量原型决策片段例外。 | **中**。可合并成运行前准备步骤；明确已有 seam 决定，减少重复确认。 |
| [to-tickets][skill-to-tickets] · U | spec/计划太大，需要可独立验证、适合一个新上下文的纵向切片。 | 一票一文件或 tracker issue，验收标准与 blocking edges；必要时 sub-issue/native dependencies。 | 人审拆分粒度、依赖、合并/拆分，批准后才发布；本地写 `.scratch/<feature>/issues/NN-*.md`；不关闭/修改 parent；宽范围机械重构用 expand–contract。 | **中**。保留切片与依赖原则；和 to-spec 合并进入一次前置审阅，交给执行层消费 task graph。 |
| [implement][skill-implement] · U | 已有具体工作、spec 或一张票，要直接实现。 | 实现、类型检查/测试、code-review，最后提交到当前分支。 | 票引用需读取并报标题；歧义时询问；尽量在预先约定 seams 上用 tdd；定期单测/类型检查，末尾全量测试；调用 code-review 后 commit。 | **中/高**。保留为单任务执行纪律，可并入统一 worker。需要解决评审是否包含未提交改动，见后文。 |
| [implement-spec][skill-implement-spec] · U | 整份 spec 已拆票，要一次实现所有 ready frontier，而不是人逐票驾驶。 | 单一 integration branch，合并完成的 tickets；按 tracker 规则关闭，必要时 draft PR 转 ready。 | 必须 tracker、fresh subagents、每票独立 worktree/branch；可先 exploration；每个 implementer 用 tdd 并同步 integration tip；由 merger subagent 合并；总评审后 fresh implementer 修问题、清理 worktrees。 | **高，但依赖宿主**。已有的主要自动执行入口；保留其 task graph/隔离/总评审思想。它没有附带持久队列、租约、崩溃恢复、重试与预算执行器。 |
| [wayfinder][skill-wayfinder] · U | 绿色项目或巨大模糊工作，连路线都装不进一次会话。 | tracker 中的 map、decision tickets、依赖、resolution comments 与决策索引。 | 主要是计划，默认不做交付；grilling/prototype 为 HITL、research 为 AFK；除研究外每会话最多解决一票；可并行研究，需 subagents、tracker 操作/claim。 | **低**。仅巨大且模糊的任务按需使用；不适合作为普通 feature 的常规流水线。 |
| [retro][skill-retro] · U | 会话后找环境问题，尤其走偏或重复犯错。 | 按严重度排序的导航、检查、标准、工具、信息可达性改善建议。 | 调用 writing-for-agents，读会话原始记录和已有 check/CI；机械错误优先确定检查、判断问题才写 coding standards。默认是向用户呈现候选，不自动全面改环境。 | 分析 **高**。按需/采样；保留“错误变检查”的反馈思想，避免每次都展开环境改造。 |
| [prototype][skill-prototype] · M | 纸上讨论答不出状态/逻辑是否合理，或 UI 应该长什么样。 | 逻辑单 HTML demo，或同一路由可切换的多种 UI；将结论与原型 branch 指针留在 issue。 | 根据问题选择 LOGIC/UI；尽量一命令启动、内存状态、无测试与过度抽象；最终原型保留在 main 外的 throwaway branch，而非生产代码。 | 生成 **高**、评判 **低**。按需；不要在已决定的任务中自动加原型阶段。 |
| [diagnosing-bugs][skill-diagnosing-bugs] · M | 难 bug、间歇性失败、性能退化。 | 已跑过且针对原症状会红的快速反馈命令、最小复现、排序假设、修复/回归证据、清理。 | 无反馈 loop 必须停止并说明；可 test/curl/CLI/browser/replay/fuzz/bisect，最后才人点操作的 HITL 模板；展示假设但用户 AFK 不阻塞；日志/产物脱敏；无正确测试 seam 要记录。 | **高**，前提是环境可达。保留核心质量纪律；这是主动建立可运行反馈，不是只读代码猜原因。 |
| [research][skill-research] · M | 文档、官方 API、规范或外部事实需要查清。 | 单份有来源的仓库 Markdown 研究文件。 | 必须后台 fresh agent，使用第一手资料；读写目标目录需可用；主代理可继续独立工作。 | **高**。保留。必须适配宿主 subagent API，避免递归套研究造成无限 fan-out。 |
| [tdd][skill-tdd] · M | 构建已知行为、修复 bug，用户要 test-first 或 integration tests。 | 一个行为切片一轮的 red→green 代码与公共接口测试。 | 写测试前必须约定并确认 seams；可调用 codebase-design；引用 tests/mocking 指南；禁止 implementation-coupled、tautological、一次写完全部测试。当前明确把 refactor 留到 review。 | **中/高**。保留测试质量与逐片反馈；运行前约定 seams 后可连续执行，不能照原文声称全程无人工。 |
| [domain-modeling][skill-domain-modeling] · M | 术语冲突、概念模糊、领域关系或确需 ADR。 | 即时更新 glossary/少量 ADR；多上下文支持 glossary map。 | 主动质疑人的说法并对照代码、用具体反例澄清；文档按需创建；ADR 要同时满足难逆转、无上下文难理解、有真实取舍。 | **中**。保留作按需的领域语言纪律；不必把每次读 glossary 都升级成建模访谈。 |
| [codebase-design][skill-codebase-design] · M | 模块接口、seam、可测试性或深模块设计需要共同语言。 | 设计约束与术语；按需 deepening 或 design-it-twice 比较。 | 主要是 reference，不是必须跑完整会话；支持多 fresh agents 提出不同接口；强调少接口、多行为、locality、测试跨同一 seam。 | **高**。保留为设计参考，可与 review/test 的标准共用，不额外增加人工阶段。 |
| [code-review][skill-code-review] · M | 自固定点以来的 branch/PR 需要标准和 spec 两轴评审。 | 分开的 Standards/Spec 报告及各轴计数；不跨轴混合重排。 | 固定点缺失要问；需非空三点 HEAD diff；查 spec 找不到要问；tracker 缺失指向 setup；fresh 两 subagents 并行；标准轴有 Fowler smell baseline，工具已覆盖的跳过；无 spec 可跳该轴。 | **高**，输入齐全时。保留独立审查；需明确评审对象并把 findings→修复→复核闭环放到执行层，而非把报告生成当质量门已强制。 |
| [pr][skill-pr] · M | 写 PR body 时自动使用。 | 最小视觉解释 + before/after evidence + Door/Blast Radius。 | 依赖真实测试/截图证据与 glossary 词汇；本身只规定写作形状，不创建、合并或运行评审。 | **高**。保留/合并为交付模板，避免为小改强制复杂图。 |
| [wizard][skill-wizard] · M | 真正只有人能完成的凭据、控制台、一次迁移/切换。 | 从 bundled template 派生的交互 Bash wizard 与运行说明。 | 先确认阶段、值来源/去向/是否保密；可写 env、`gh secret`/variable；不可逆动作确认；只静态核验与 bash -n/shellcheck，不由代理端到端运行。 | **低**，刻意是 HITL。按需；作为阻塞点的完整交付，不应塞进普通自动实现路径。 |

### 生产力：7 项，正式发布

| 技能 | 用途与触发场景 | 主要输出 | 交互、依赖与副作用 | 无人值守适配与初步取舍（待决） |
| --- | --- | --- | --- | --- |
| [grill-me][skill-grill-me] · U | 没有工作目录的想法、计划或写作，要经受访谈。 | 不持久化的共同理解。 | 只是调用 grilling；持续等用户决定；有工作目录时 ask-matt 推荐 grill-with-docs。 | **低**。按需；与 grill-with-docs 可在用户入口层合并为“是否保存领域文档”的选择。 |
| [grilling][skill-grilling] · M | 压测思考、穷尽设计树；其他技能可复用的访谈原语。 | 一轮问可回答的全部 frontier，带推荐答案，直到决策清空。 | 环境事实由 fresh subagent 查，决定交给用户并等待；全部达成后仍要用户确认共同理解，才行动。 | **低**。保留为需求不清时的工具，绝非无人值守 worker 的默认步骤。 |
| [handoff][skill-handoff] · U | 换宿主、目录、同事或分叉侧任务，需要可携带上下文。 | OS temp 里的 Markdown handoff，含 suggested skills、资料路径/URL、脱敏信息。 | 本身只写文件，不启动/排队/监督下一代理；已有 artifacts 用指针不复制。 | 生成 **高**，接续需宿主。按需保留；同宿主连续任务不必每阶段人工 handoff。 |
| [teach][skill-teach] · U | 多会话学习一项技能/概念。 | MISSION/RESOURCES/学习记录、交互 HTML lessons、reference、共享 assets。 | 需厘清学习动机、尊重当前程度、找可信资料；用户实践/提问是核心；可建议真实社区。 | 对代码无人值守目标 **低相关**。按需，放独立教学工作区。 |
| [to-questionnaire][skill-to-questionnaire] · U | 关键知识在第三方脑中，需要异步问卷。 | 当前目录 `to-questionnaire-<slug>.md`，含目的、对象、截止/工作量、主题问题与回答空位。 | 两次核心交换确认“发给谁”和“要拿回什么”；不会代发给第三方。 | **低**。按需；是解决外部信息阻塞的产物，不是运行器。 |
| [wait-what][skill-wait-what] · U | 上一条解释没讲明白，立即要求重述。 | 补上下文、简化英语、使用 glossary 的重述。 | 必须人发现不懂并触发；源码指向 ASD-STE100 English，中文工作流需另行适配。 | **低相关**。按需帮助入口；不要加到自动代码路径。 |
| [writing-for-agents][skill-writing-for-agents] · M | 写 skill、AGENTS/CLAUDE 或代理通过指针读取的文档。 | 更明确的 trigger、步骤、完成条件和按需 reference；减少重复与无效说明。 | 作为参考，区分 context load / human cognitive load；技能分拆与 router 另读 SKILL-MECHANICS。 | **高**。保留，用来改造整套编排说明；不是再次叠一层流程。 |

### Misc：4 项，不正式发布且已冻结

| 技能 | 用途与触发场景 | 主要输出 | 交互、依赖与副作用 | 无人值守适配与初步取舍（待决） |
| --- | --- | --- | --- | --- |
| [git-guardrails-claude-code][skill-git-guardrails-claude-code] · M | 希望 Claude Code 拦截 push/reset/clean 等 Git 命令。 | Claude PreToolUse/Bash hook、settings 修改与一次拦截验证。 | 询问项目/全局范围与定制；hook 脚本依赖 bash、jq、grep；只匹配命令字符串。不是 Codex 通用策略，亦非严密 shell 解析。 | **不采纳为安全边界**。若需 Claude 局部提醒可按需修复；无人值守硬权限应由宿主/凭据/仓库规则落实。 |
| [migrate-to-shoehorn][skill-migrate-to-shoehorn] · M | TS 测试里 `as`/double-as/大对象 fixture 太多。 | 安装 `@total-typescript/shoehorn` 并替换测试造数据写法，运行 typecheck。 | 先问范围与错误输入需求；仅限测试，禁止生产代码；原文用 npm install，不适配所有项目依赖约定。 | **中/高**。按需单次迁移；不作为所有测试的必经工具，也不为无人值守而普遍增依赖。 |
| [scaffold-exercises][skill-scaffold-exercises] · M | Matt 风格课程 sections/exercises 脚手架。 | `exercises/XX-*/XX.YY-*/{problem,solution,explainer}/readme.md`，lint 后 commit。 | 强依赖 `pnpm ai-hero-cli internal lint` 与课程目录规则；移动用 git mv；可自动提交。 | 对当前代码目标 **不采纳默认安装**。做相同课程时按需。 |
| [setup-pre-commit][skill-setup-pre-commit] · M | 想加 Husky + lint-staged + Prettier + typecheck/test hook。 | 新依赖、配置、`.husky/pre-commit`，最后 stage/commit。 | 根据已有包管理器适配；缺 typecheck/test 要报告并省略；实际项目可能已有 Biome/其他检查；本身 frozen。 | **中**。合并“接线已有确定检查”的目的，按仓库工具实现；不直接套统一 Husky/Prettier 配方。 |

`git-guardrails` 的已知边界有上游自身依据：冷冻政策列出 `git -C` 绕过、缺 jq 时 fail-open 等既往报告；本次静态阅读的脚本确实是 regex 黑名单且结尾 `exit 0`，没有完备解析或 jq 错误处理。本报告没有执行它，也不声称测试了所有绕过。[冷冻政策][frozen]、[hook 源码][git-hook]

### In-progress：8 项，公开 beta，不在正式 plugin

| 技能 | 用途与触发场景 | 主要输出 | 交互、依赖与副作用 | 无人值守适配与初步取舍（待决） |
| --- | --- | --- | --- | --- |
| [chief-of-staff][skill-chief-of-staff] · U | 一个长期目标，需要在单个长期会话中协调多代理并改善后续环境。 | 子代理成果、任务推进、互链 Markdown wiki；建议可用的 recurring schedules。 | 全部工作交 subagents，fresh context、稀疏通信与 pointers；没有共享 wiki 才先约定位置；约每五次子会话做 retro；大工作走 spec/tickets/implement-spec。持久知识需日期/commit/来源。 | **中/高但 beta**。合并其分工、wiki 与环境改进思想，暂不原样承担可靠调度中枢；无可执行恢复器，并存在调用/目录约定张力，见后文。 |
| [claude-handoff][skill-claude-handoff] · U | 当前对话要马上交给后台的新 Claude agent。 | 临时 handoff 文件，加 `claude --bg --name ...` 启动的后台代理；用户用 `claude agents` 管理。 | 真正调用外部 Claude CLI，依赖该版本支持 `--bg`；总结须脱敏与引用 artifacts；不是通用 Codex handoff。 | **中**。按需跨宿主桥接，需先验证 CLI；不默认作为故障恢复或持续队列。 |
| [loop-me][skill-loop-me] · U | 找出生活/工作的重复 loop，设计可委托 workflow。 | `workflows/*.md` 的可实现规格和记录世界/术语的 `NOTES.md`。 | 持续 grilling，直到实现者不再需要提问；定义 Trigger/Checkpoint/Brief/Push right。明确不强制 AI、检查点或 schedule。 | 设计 **低**，结果可支持自动化。按需/合并为一次性 workflow 设计；它不执行这些 workflows。 |
| [setup-ts-deep-modules][skill-setup-ts-deep-modules] · U | TS 仓库想把 package 实现藏在子目录，只经根文件 entry points 调用。 | dependency-cruiser 依赖、边界配置、check 接线、示例 package、目录 README 与 agent pointer。 | 调用 codebase-design；四条 error 规则含无环、外部只经 entry、测试只经 entry；必须观测 clean pass→违规 fail→恢复 pass。约定单层平坦 packages，可能与现有架构不合。 | **中**。保留“证明规则真会失败”的方法；只在架构匹配时按需落地，不把通用 deep-module 思想等同此目录模板。 |
| [software-factory][skill-software-factory] · U* | 设计从 tickets/PR/schedules 到 merged code 的远程代理工厂。 | 服务选型和 task/run/trigger/去重/人介入的完整设计，不是部署好的工厂。 | 含 5 篇参考，需根据用户实际问题与当前产品研究填写服务槽；强调 checks、独立 review、前期每 PR 人审、循环限次。该项本地未装且无 openai.yaml。 | 设计参考 **高相关**。建议借用概念，与拟引入编排层对齐；**不将安装它视为自动化已实现**。 |
| [writing-fragments][skill-writing-fragments] · U | 写作探索阶段，挖素材而不定结构。 | 单 Markdown 素材文件，仅 H1 与水平线分片。 | 持续采访；路径未知问一次；从初始话语捕捉；每次写前重读并保留用户改动，默认静默 append。 | 对代码目标 **不采纳默认路径**。写作时按需。 |
| [writing-shape][skill-writing-shape] · U | 已有素材，逐段形成有论点的文章。 | 与原材料分开的文章文件。 | 先全文读素材、定读者前提、给多种开篇让人选；每段讨论内容/形式，用户决定何时结束；不改原料。 | **低**。写作按需；不作为工程文档的自动模板。 |
| [writing-beats][skill-writing-beats] · U | 由固定素材拼出逐 beat 的阅读旅程。 | 一次只追加一个已选 beat 的文章，维护已 grounding 概念。 | 定读者前提，反复给 2–3 条可走路径让人选择；写前重读。与 writing-shape 同属 exploit，但粒度是 beat/路径选择。 | **低**。写作按需；可在用户入口层与 writing-shape 合并选择，不加入无人值守编码。 |

## 对无人值守最关键的依赖与交互

### 哪些环节强依赖人

- **连续访谈/选择**：grilling、grill-me、grill-with-docs、wayfinder 的 HITL tickets、loop-me、三项 writing beta、teach。它们的价值就在取得人的判断，不能把“回答自己的问题”伪装为自动化。[grilling][skill-grilling]、[wayfinder][skill-wayfinder]
- **一次或少量前置确认**：setup 的仓库约定、to-spec/tdd 的测试 seams、to-tickets 的拆票/依赖、architecture 的候选选择、wizard 的阶段。这些可以集中在任务开始前，只有新增不确定性才再找人；这是组合建议，原文没有提供自动跳过所有确认的模式。[setup][skill-setup-matt-pocock-skills]、[tdd][skill-tdd]、[to-tickets][skill-to-tickets]
- **不默认阻塞的说明**：diagnosing-bugs 要展示假设，但明确用户 AFK 时继续按排序验证。prototype 在用户不可达时，可依据代码上下文选择逻辑/UI，并声明假设。[diagnosing-bugs][skill-diagnosing-bugs]、[prototype][skill-prototype]
- **原则上必须人在场的手工步骤**：wizard 的运行；凭据/外部控制台访问可能是根本阻塞。它的目标是让人一次看清并做完，而非代理假装已完成。[wizard][skill-wizard]

### 哪些依赖 tracker、CLI、子代理

| 依赖 | 明确涉及的技能/边界 |
| --- | --- |
| 配置的 tracker/标签 | setup、to-spec、to-tickets、triage、implement-spec、wayfinder；code-review 要 tracker/规格来源；implement 传 ticket 时读取；prototype 最终结论/branch 指针落在 issue。不是一律 GitHub：本地 Markdown 是正式模板，其他 tracker 可记录自定义流程。 |
| Git/分支/worktree | implement 自动 commit；implement-spec 多 worktree 与集成分支；code-review 依赖 Git 固定点/committed diff；prototype 保留非 main 的原型分支；wayfinder 研究可推独立 research branch；misc 有自动 commit/hook。 |
| 外部 CLI/工具 | GitHub 模板依赖 gh，GitLab 模板依赖 glab；claude-handoff 依赖 Claude CLI 的后台 agent 能力；wizard 使用 Bash，可写 gh secrets；misc 分别依赖 jq/grep、npm/shoehorn、pnpm ai-hero-cli、Husky/Prettier；TS beta 依赖 dependency-cruiser。 |
| 明确 fresh subagents | research、code-review、implement-spec、architecture；grilling 查环境事实；wayfinder 的并行 research；chief-of-staff 全部工作；codebase-design 的可选 design-it-twice。派多少、嵌套多深、能否后台和持久运行由宿主决定。 |

以上依赖逐项来源均在前述技能链接。tracker 的真实操作约定见 [GitHub 模板][tracker-github]、[本地模板][tracker-local]。上游明确拒绝把子代理递归上限写进每个 skill，认为应由 harness 限制；因此不能推定此仓库天然保证 fan-out 有界。[subagent recursion 政策][recursion]

## 已有“自动化”入口，究竟做到哪里

| 入口 | 上游确实提供 | 不能据此推定已提供 |
| --- | --- | --- |
| implement-spec | 依赖图 frontier、并行 implementers、独立 worktree、merger、总 review 与一次修复阶段。 | 持久 scheduler、原子 ticket 租约、进程重启恢复、预算上限、幂等 merge/retry 引擎。源码是 42 行 prompt，不是此类执行器实现。 |
| chief-of-staff | 长期会话协调、Markdown wiki、宿主允许时建议 schedules、持续环境改进。 | 无人干预跨崩溃运行、确定性的状态迁移、定时器一定会安装并执行。 |
| handoff | 可携带且脱敏的交接文件。 | 后继一定启动、接棒成功、状态回写或持续监督。 |
| claude-handoff | 写摘要并调用外部 CLI 立即启动后台 Claude。 | 通用 Codex 支持、重启恢复与可重试队列。 |
| loop-me | 把一个重复 loop 定义成实现者无需追问的 workflow spec；检查点尽量推迟。 | 执行 workflow、监听事件、安装 schedules。 |
| software-factory | 工厂设计语言、服务槽位、task 设计问题、示例链和质量制动。 | 一套已部署的工厂、生产 runner/queue、与 pstack 的现成集成。 |

本表右栏是对源码/文件树的静态判断，不是失败测试结论。skill 可以指导代理编写这些缺失机制，但它们不会因为技能已安装而自动存在。[implement-spec][skill-implement-spec]、[factory 文件树][factory-tree]

### software-factory 的价值与限制

它最贴近本次目标，但不是“安装即用”的替代工具。它规定一个 run 遇到人类决定时应结束，人的后续 ticket/PR 更新触发新 run；runner 可丢弃，跨 run 记忆在 tracker、git host 和 orchestrator。这个模型比让单一聊天无限等待，更适合事件驱动的可恢复系统设计。[软件工厂定义][skill-software-factory]

其 5 篇支撑文档的职责分别是：

| 文档 | 内容 | 本次可直接借用的部分 |
| --- | --- | --- |
| [EXAMPLE-TASKS.md][factory-examples] | explore→implementer→automated review→rework；decompose、每日 ratchet、monitor intake、失败 fix、architecture、retro。 | 任务职责与后继事件；失败修复自链要截止，review/rework 有次数上限。 |
| [TICKET-TRACKERS.md][factory-trackers] | 按 git-host、开发团队 SaaS、自托管、通用工作台、repo-native、自建分类。 | 对 trigger、routing、comments、identity、外部报单与 hosting 的选型问题。 |
| [GIT-HOSTS.md][factory-git] | git 平台、套件、自托管、特殊 review 模型、agent-native、临时 git 存储。 | bot identity、required checks/approvals、webhook、rate budget 和能填哪些槽。 |
| [RUNNERS.md][factory-runners] | CI runner、MicroVM、bundled agent、BYO worker、自有容器/VPS。 | 谁拥有 agent loop/机器、如何启动、timeout/concurrency、可达网络、如何可丢弃。 |
| [OBSERVABILITY-PLATFORMS.md][factory-observability] | 无独立平台、agent tracing、APM、gateway；5 种数据接入方式。 | 先问现有 run 页面是否足够，再考虑跨 run 搜索、成本、保留期与 tracing。 |

四份服务 survey 都声明调研于 **2026-10**，要求用当前一手资料重新验证产品、价格、限制和 beta 状态。本报告将它们作为技能的设计内容盘点，**没有把其中厂商能力/价格转述成 2026-11-15 的已核实事实**。本次也没有替用户选定云服务。

### 应在组合前澄清的源码张力

1. **实施后的评审对象不够明确。** implement 要 code-review 后才 commit；code-review 指定 `git diff <fixed-point>...HEAD`，只覆盖 committed HEAD，不覆盖未提交 working tree/index。对自动 worker，要规定先做可审查的 checkpoint commit，或明确传入包含未提交改动的 diff。否则“调用过 review”不等于“审过刚写的代码”。这是静态流程不一致，尚未运行复现。[implement 第 15–17 行][review-order]、[code-review 第 19–23 行][review-diff]
2. **TDD 的实际步骤比 README 的概括更窄。** SKILL 明说仅 red→green，refactor 归 review 阶段；不能按习惯把它描述成每轮完整 red-green-refactor，也不能让“只需调用 TDD”承担设计/重构闭环。[tdd 规则][tdd-rules]
3. **chief-of-staff 的跨目录指针依赖安装形状。** 上游文件在 `in-progress/chief-of-staff/`，其 `../retro`、`../to-spec`、`../to-tickets`、`../implement-spec` 在 bucket 布局中不存在；但用户本地是 `.agents/skills/<name>/` 的扁平布局，这四条指针都能解析。不能说用户现在因此坏掉；应记录可移植性假设。它直接读取并执行 user-only spec/tickets/implement-spec 的做法，还与仓库“不能从 skill 调 user-only”的调用原则存在张力。[chief procedures][chief-procedures]、[调用原则][invocation]
4. **规范意图不等于宿主已强制。** 绝大多数 skill 是自然语言步骤；`allow_implicit_invocation` 是调用策略元数据；它们不等于机器检查全部前置条件。硬约束实际落在 CI、仓库规则、hook 或宿主权限时才可验证。上游自己把子代理深度限制交给 harness；software-factory 当前还缺 Codex policy 文件。[调用规则][invocation]、[递归政策][recursion]

## 本地与当前上游的准确差异

| 核对项 | 本次结果 |
| --- | --- |
| lock schema | `version: 2`。 |
| 本地条目来源 | **38/38** 为 `source: mattpocock/skills`、`sourceType: github`。 |
| 记录版本的方式 | 每条有 `skillPath` 与 64 位十六进制 `computedHash`；**没有 commit SHA/ref/tag 或 plugin version 字段**。computedHash 不能当作 Git commit。 |
| 本地内容版本 | 38 个对应目录的路径集合和 103 个文件字节全部与本次固定上游 SHA 一致，包含 SKILL、配套 YAML、参考文件和 bundled scripts。这个事实可确定内容相同，不能恢复安装日期或原始安装 commit。 |
| 新增上游项 | 只有 **software-factory**，位于 `skills/in-progress/`；本地未装。 |
| 本地多余/上游删除项 | **0**。 |
| 已装技能的上游行为变化 | **0**，对应目录全文相同。不存在“只 SKILL 相同、参考文件不同”的情况。 |
| 发布状态差异 | 本地安装了全部 **27 正式项 + 4 frozen misc + 7 beta**，所以“已安装”不等于“已正式发布/日常维护”。 |
| 本地配置能否保证运行 | 本次只核对技能与 lock；未验证每个业务仓库的 tracker 文档、gh/glab 登录、CLI 版本、fresh context 行为与实际权限。 |

源码相同不代表各宿主实际行为相同，也不说明每次技能都会被触发。尤其 16 个正式 U 入口的人工选择负担是其设计的一部分。[本地 lock](/Users/nonlinearthink/Documents/Projects/nonlinearthink/skills/skills-lock.json)、[上游调用设计][invocation]

## 面向目标的初步组合建议（全部待决）

这不是马上删除或安装的清单；先按职责收敛，再与 pstack 的真实能力对照。

| 决策方向 | 候选 | 理由与边界 |
| --- | --- | --- |
| **保留质量纪律** | diagnosing-bugs、tdd、code-review、codebase-design、research、writing-for-agents。 | 确切症状的反馈、正确测试 seam、独立标准/spec 审查、设计参考、一手来源。它们改善代码质量，额外编排层应复用这些约束。 |
| **合并入口/阶段** | to-spec + to-tickets 的前置准备；implement/implement-spec 的执行职责；pr 的交付形状。 | 人一次审范围、验收、seams、拆票/依赖，形成可消费任务；随后 worker 执行与独立 review。保留产物与质量门，减少用户记忆 slash-command 和阶段切换的成本。 |
| **合并为接入与反馈职责** | setup 的每仓库配置；retro 的采样分析；setup-pre-commit 的确定检查目的；chief 的历史 wiki/pointers 思想。 | 配置只做一次；机械错误转检查；已有工具优先；避免每次任务重复建系统。 |
| **按需保留** | grilling/grill-with-docs/grill-me、domain-modeling、prototype、architecture、wayfinder、triage、wizard、handoff、to-questionnaire、teach、wait-what。 | 只在需求不清、外部信息/人为步骤、架构风险或交接时加入；不设成所有改动的强制关卡。 |
| **按需研究/借用，暂不原样当执行中枢** | chief-of-staff、loop-me、software-factory、claude-handoff、setup-ts-deep-modules。 | 与无人值守有关系，但分别是 beta 提示词、workflow 规格、工厂语言、特定 CLI 桥、特定 TS 架构模板。应先验证最关键宿主能力。 |
| **不采纳默认编码流程** | 三项 writing beta、scaffold-exercises、migrate-to-shoehorn。 | 它们是内容/课程/特定测试迁移工具，和本次目标正交；有具体任务再调用。 |
| **不采纳为硬安全边界** | git-guardrails-claude-code 原版。 | frozen、Claude 专用、字符串匹配不完整；应由权限、token scope、branch protection 和确定检查形成可验证边界。 |

对未来编排层的最小验收问题来自上述缺口，而非要求再叠一整套人工流程：任务状态和验收能否持久化；并发执行是否有占用与隔离；review 能否读到正确 diff；失败重试是否有上限且可继续；需要人时能否以决策 brief 结束、回填后重启；checks/review 是否真正阻止不合格交付。这些都是**后续比较项**，不是本报告已经验证 pstack 具备的能力。

## 许可与复用

仓库为 **MIT License，Copyright (c) 2026 Matt Pocock**。对复制或修改后的 substantial portions 保留版权与许可声明；可以在此基础上维护自用组合。这里记录许可原文信息，不展开法律判断。[LICENSE][license]

## 复核方法与来源索引

本次通过自写只读 Python 比较两边每个技能目录的相对文件集合和文件字节；不是用 lock 的 hash 猜测版本。全仓枚举包括隐藏目录，得到 39 个 SKILL；逐个读完后才写表。没有运行上游 npm scripts、link-skills.sh、shell templates、Claude CLI、Git hooks 或任何 tracker 写操作；没有修改 `.agents/skills` 或 `skills-lock.json`，没有提交。

除下列本地快照链接外，所有来源均固定到同一个上游 SHA，避免随 main 漂移。

[repo-tree]: https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa
[commit]: https://github.com/mattpocock/skills/commit/5863806dd4e15c63174bee4e7515a4256792ecfa
[package]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/package.json
[manifest]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.claude-plugin/plugin.json
[invocation]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/invocation.md
[mechanics]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/writing-for-agents/SKILL-MECHANICS.md
[repo-agents]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/AGENTS.md
[scope]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/SCOPE.md
[frozen]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.out-of-scope/frozen-misc-skills.md
[beta-readme]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/README.md
[factory-tree]: https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory
[git-hook]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh
[recursion]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.out-of-scope/subagent-recursion.md
[tracker-github]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md
[tracker-local]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md
[factory-examples]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory/EXAMPLE-TASKS.md
[factory-trackers]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory/TICKET-TRACKERS.md
[factory-git]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory/GIT-HOSTS.md
[factory-runners]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory/RUNNERS.md
[factory-observability]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory/OBSERVABILITY-PLATFORMS.md
[review-order]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/implement/SKILL.md#L15-L17
[review-diff]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/code-review/SKILL.md#L19-L23
[chief-procedures]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/chief-of-staff/SKILL.md#L49-L54
[tdd-rules]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/tdd/SKILL.md#L34-L38
[license]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/LICENSE
[skill-ask-matt]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/ask-matt/SKILL.md
[skill-code-review]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/code-review/SKILL.md
[skill-codebase-design]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/codebase-design/SKILL.md
[skill-diagnosing-bugs]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/diagnosing-bugs/SKILL.md
[skill-domain-modeling]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/domain-modeling/SKILL.md
[skill-grill-with-docs]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/grill-with-docs/SKILL.md
[skill-implement]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/implement/SKILL.md
[skill-implement-spec]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/implement-spec/SKILL.md
[skill-improve-codebase-architecture]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/improve-codebase-architecture/SKILL.md
[skill-pr]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/pr/SKILL.md
[skill-prototype]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/prototype/SKILL.md
[skill-research]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/research/SKILL.md
[skill-retro]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/retro/SKILL.md
[skill-setup-matt-pocock-skills]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/setup-matt-pocock-skills/SKILL.md
[skill-tdd]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/tdd/SKILL.md
[skill-to-spec]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/to-spec/SKILL.md
[skill-to-tickets]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/to-tickets/SKILL.md
[skill-triage]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/triage/SKILL.md
[skill-wayfinder]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/wayfinder/SKILL.md
[skill-wizard]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/wizard/SKILL.md
[skill-chief-of-staff]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/chief-of-staff/SKILL.md
[skill-claude-handoff]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/claude-handoff/SKILL.md
[skill-loop-me]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/loop-me/SKILL.md
[skill-setup-ts-deep-modules]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/setup-ts-deep-modules/SKILL.md
[skill-software-factory]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/software-factory/SKILL.md
[skill-writing-beats]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/writing-beats/SKILL.md
[skill-writing-fragments]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/writing-fragments/SKILL.md
[skill-writing-shape]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/writing-shape/SKILL.md
[skill-git-guardrails-claude-code]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/misc/git-guardrails-claude-code/SKILL.md
[skill-migrate-to-shoehorn]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/misc/migrate-to-shoehorn/SKILL.md
[skill-scaffold-exercises]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/misc/scaffold-exercises/SKILL.md
[skill-setup-pre-commit]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/misc/setup-pre-commit/SKILL.md
[skill-grill-me]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/grill-me/SKILL.md
[skill-grilling]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/grilling/SKILL.md
[skill-handoff]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/handoff/SKILL.md
[skill-teach]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/teach/SKILL.md
[skill-to-questionnaire]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/to-questionnaire/SKILL.md
[skill-wait-what]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/wait-what/SKILL.md
[skill-writing-for-agents]: https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/writing-for-agents/SKILL.md
