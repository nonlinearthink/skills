# octo-mode skills

以 [mattpocock/skills](https://github.com/mattpocock/skills) 为基础，补充自动选路、流程串联和按需澄清等能力，让 Codex 与 Claude Code 的开发流程更自动化、更好用。

这不是上游的 fork 或替代品。上游继续提供需求澄清、规格、实现、诊断、TDD、审查等工程方法与质量纪律；本仓库补充减少人工操作的编排与专用能力。

## 目标

- **少选**：从用户意图和任务上下文自动选择流程，不要求用户先记住每个 skill 的入口。
- **少串**：在已授权范围内自动衔接调查、实现、验证、独立审查、修复与交付。
- **少问**：事实自行调查，可逆的实现选择自行决定；只追问缺失的产品/验收决定和不可逆取舍。完整 grilling 仅在用户明确要求深挖时启用。
- **按任务展开**：小任务直接完成，复杂任务才引入完整规格、任务拆分和并行协调，避免固定走重型流程。
- **保留质量门**：复用 Matt 的工程纪律，以真实验证和独立审查支撑交付，而不是以流程执行完毕代替结果验证。
- **跨宿主**：共享同一套流程语义，分别处理 Codex 与 Claude Code 的调用和运行能力差异。

默认交付终点是已验证、已独立审查的 PR；只有项目或任务明确授权时才自动合并。首版聚焦用户启动的单项任务持续推进，跨进程自动恢复和事件驱动自动接单不属于首版承诺。

[pstack](https://github.com/cursor/plugins/tree/main/pstack) 作为自动路由、完成判据、验证和恢复机制的参考，不与 Matt 并列为本仓库的基础，也不整套移植。

## 当前状态

本地源码已新增统一入口 `octo-mode` 初版，负责从目标选路，衔接 Matt 的工程方法与质量闭环。它是 prompt 驱动的编排 skill，首版覆盖当前任务推进和接续记录；宿主触发、实际验证与已测范围见 [验证记录](tests/octo-mode/validation.md)。远程安装需要对应源码先推送到 GitHub。

- [设计讨论与已确认决定](docs/design/development-skills-session.md)
- [统一入口与需求澄清候选方案](docs/design/01-entry-and-clarification.md)
- [领域词汇表](GLOSSARY.md)

## 安装

使用完整开发流程时，先按 [mattpocock/skills](https://github.com/mattpocock/skills) 的说明安装基础 skills，再安装本仓库的补充 skills。下表中的独立 skills 也可按需单独使用。

在需要使用 skill 的项目目录运行：

```bash
npx skills add https://github.com/nonlinearthink/skills
```

按提示选择 skill 和目标 agent。默认安装到当前项目；添加 `-g` 可全局安装。

试用尚未推送的本地 `octo-mode` 源码，可在本仓库运行：

```bash
npx skills add ./skills --skill octo-mode -a codex claude-code
```

该命令安装到当前仓库。要在其他项目中使用，可在目标项目传入本仓库 `skills/` 的绝对路径，或加 `-g` 全局安装。

安装到目标 agent 后，在项目中给目标即可，例如 Codex 中输入 `$octo-mode 修复登录重试失败的问题`，Claude Code 中输入 `/octo-mode 修复登录重试失败的问题`。入口也支持自动发现；显式调用可确保选择本流程。上游部分入口只允许用户主动调用，因此 `octo-mode` 使用自身的阶段适配协议，具体差异见 [上游适配规则](skills/octo-mode/references/upstream.md)。

查看可安装的 skills：

```bash
npx skills add https://github.com/nonlinearthink/skills --list
```

## Skills

| Skill | 用途 |
| --- | --- |
| [octo-mode](skills/octo-mode/SKILL.md) | 从开发目标自动路由，按需衔接调查、规格与依赖图、实现、验证、独立审查、修复和 PR 交付；支持只读与本地交付边界。 |
| [regression-testing](skills/regression-testing/SKILL.md) | 根据行为与契约传播分析变更影响，只选择影响面内的用例及项目明确要求的门禁，编排执行并验证覆盖与停止边界。 |
| [test-gardening](skills/test-gardening/SKILL.md) | 盘点、去重和清理手工及自动化用例，按风险建立核心、模块、全量分层和最小发布回归集，评估自动化候选。 |
| [ui-design](skills/ui-design/SKILL.md) | 编写或修改页面、组件、布局、样式、交互和界面文案，兼顾任务完成、产品视觉识别与信息层级。 |

`regression-testing` 和 `test-gardening` 的回归分层、变更影响面、最小发布回归集、用例清理、入口出口和自动化取舍原则参考了 PingCode 的[《回归测试耗时太长怎么办？实操清单》](https://docs.pingcode.com/insights/a784hn5m0ja8casoo7cyhn06)，并补充了代码级传播追踪、选择核对与证据要求。

`ui-design` 的视觉方向、排版、动效与自检原则参考了 Anthropic 的 [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)（[UI Skills 页面](https://www.ui-skills.com/skills/anthropics/frontend-design)），结合本 skill 的任务导向与局部修改范围整理。

## 维护

每个 skill 的源码放在 `skills/<skill-name>/`：

```text
skills/
├── octo-mode/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── scripts/resolve_matt.py
│   └── LICENSE-Matt-Pocock.txt
├── regression-testing/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/project-test-map.md
├── test-gardening/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/gardening-checklist.md
└── ui-design/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

新增 skill 时创建对应目录，编写带有 `name` 和 `description` YAML frontmatter 的 `SKILL.md`。名称与目录名一致，使用小写字母、数字和连字符。需要时再添加 `agents/`、`references/`、`scripts/` 或 `assets/`。

提交前检查发现结果：

```bash
npx skills add ./skills --list
```

`octo-mode` 的定位脚本回归：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/octo-mode -v
```

将更新推送到 GitHub 后，远程安装命令即可获取。`.agents/skills/`、`.claude/skills/` 和 `skills-lock.json` 用于本地安装，已在 Git 中忽略；维护和发布时修改 `skills/` 下的源码。
