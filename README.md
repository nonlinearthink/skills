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

## Skills

| Skill | 用途 |
| --- | --- |
| [ui-design](skills/ui-design/SKILL.md) | 编写或修改页面、组件、布局、样式、交互和界面文案，让用户看清状态、找到下一步并完成任务。 |

## 维护

每个 skill 的源码放在 `skills/<skill-name>/`：

```text
skills/
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
