# Personal skills

维护自己的 Agent Skills，可通过 [Skills CLI](https://github.com/vercel-labs/skills) 安装到 Codex、Claude Code 等支持的 agent。

## 安装

在需要使用 skill 的项目目录运行：

```bash
npx skills add https://github.com/nonlinearthink/skills
```

按提示选择 skill 和目标 agent。默认安装到当前项目；添加 `-g` 可全局安装。

只安装 `ui-design`：

```bash
npx skills add https://github.com/nonlinearthink/skills --skill ui-design
```

查看可安装的 skills：

```bash
npx skills add https://github.com/nonlinearthink/skills --list
```

只安装 `regression-testing`：

```bash
npx skills add https://github.com/nonlinearthink/skills --skill regression-testing
```

只安装 `test-gardening`：

```bash
npx skills add https://github.com/nonlinearthink/skills --skill test-gardening
```

## Skills

| Skill | 用途 |
| --- | --- |
| [regression-testing](skills/regression-testing/SKILL.md) | 根据行为与契约传播分析变更影响，只选择影响面内的用例及项目明确要求的门禁，编排执行并验证覆盖与停止边界。 |
| [test-gardening](skills/test-gardening/SKILL.md) | 盘点、去重和清理手工及自动化用例，按风险建立核心、模块、全量分层和最小发布回归集，评估自动化候选。 |
| [ui-design](skills/ui-design/SKILL.md) | 编写或修改页面、组件、布局、样式、交互和界面文案，兼顾任务完成、产品视觉识别与信息层级。 |

`regression-testing` 和 `test-gardening` 的回归分层、变更影响面、最小发布回归集、用例清理、入口出口和自动化取舍原则参考了 PingCode 的[《回归测试耗时太长怎么办？实操清单》](https://docs.pingcode.com/insights/a784hn5m0ja8casoo7cyhn06)，并补充了代码级传播追踪、选择核对与证据要求。

`ui-design` 的视觉方向、排版、动效与自检原则参考了 Anthropic 的 [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)（[UI Skills 页面](https://www.ui-skills.com/skills/anthropics/frontend-design)），结合本 skill 的任务导向与局部修改范围整理。

## 维护

每个 skill 的源码放在 `skills/<skill-name>/`：

```text
skills/
├── regression-testing/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/project-test-map.md
├── test-gardening/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/test-case-inventory.md
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

将更新推送到 GitHub 后，远程安装命令即可获取。`.agents/skills/`、`.claude/skills/` 和 `skills-lock.json` 用于本地安装，已在 Git 中忽略；维护和发布时修改 `skills/` 下的源码。
