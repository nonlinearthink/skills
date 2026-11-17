# 上游方法与宿主适配

适配基线：[mattpocock/skills @ 5863806](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa)，2026-11-16 核对的 main。方法的名称、文件路径和基线哈希见 [upstream.json](upstream.json)。许可见 [LICENSE-Matt-Pocock.txt](../LICENSE-Matt-Pocock.txt)。这是本仓库的补充入口，非 Matt 官方技能。

## 调用边界

上游把 `to-spec`、`to-tickets`、`implement`、`implement-spec` 等标为 user-invoked；`ask-matt` 仅导航。`octo-mode` 不尝试调用这些被禁用的入口，也不修改其元数据，而是在 [workflows.md](workflows.md) 中执行改编后的规划与协调协议。

`tdd`、`diagnosing-bugs`、`code-review` 等提供工程方法。读取选中技能的 `SKILL.md`，再读取其当前分支实际引用的支撑文件。兼容且无需调整的 model-invoked 方法可用宿主的 skill 调用能力加载；有下表调整时，通过读取源文件使用适配后的方法，并把调整传给 worker/reviewer。不能先调用完整原版再假称它没有那些要求。

用户明确单独调用上游 skill 时，保留该 skill 的独立流程；`octo-mode` 的自动流程不把用户选择重新解释为自动化授权。

## 加载与版本

先用宿主列出的技能绝对路径。需要定位时运行 `scripts/resolve_matt.py`：项目及父目录的 `.agents/skills`、`.claude/skills`、`.codex/skills`，然后全局技能目录；`--root` 可提供宿主披露的 plugin 目录或明确的上游 checkout。脚本只检查已知路径，不联网、不安装、不写文件。

- `baseline`：该入口文件与适配基线一致，仍须读实际内容及触发的支撑文件。
- `changed`：同名入口与基线不同。读取当前文件和相关支撑文件，核对调用限制、确认点、交付副作用和方法语义后再用；冲突无法消解时记录该方法不兼容。哈希只覆盖入口文件，不能证明所有支撑文件或来源均相同。
- `missing`：先检查宿主列出的插件路径并补充 `--root`。仍缺失时给出针对性的安装命令，例如 `npx skills add mattpocock/skills --skill tdd code-review`。不自动安装或覆盖用户配置；继续不依赖缺失方法的调查与准备，受影响阶段保持未完成。

同名来源优先显式指定的可信路径，再选项目约定路径；脚本列出其他匹配，避免混用不同套件的同名 `tdd`。无 Python 时按同样规则手动读取；宿主没有 “Skill tool” 时读取方法文件，不编造工具名。

## 明确的适配差异

以下只适用于 `octo-mode` 负责的目标任务，用户和项目已有要求优先：

| 上游方法/阶段 | 保留 | `octo-mode` 的调整 |
| --- | --- | --- |
| `grilling` | 事实自行查、决定给用户、按依赖提问 | 常规路径仅询问阻塞验收决定；完整访谈及其理解确认只用于明确的深度设计请求 |
| `to-spec` / `to-tickets` | 约束、行为验收、纵向切片和 blocking edges | 使用本地阶段协议；按任务规模生成产物，自选可逆拆分，不要求固定长故事、人工批准每个切片或发布 tracker |
| `implement` / `implement-spec` | 小步反馈、frontier、隔离、集成、总审查 | 使用本地阶段协议；按独立性选择串行/委派，按终点控制提交与 PR，不强制 setup 或每票 worktree |
| `tdd` | 公开接口行为测试、独立期望值、red → green、逐片实现 | 测试边界由需求、项目约定和消费方推导；已有边界不重复请用户确认。业务验收或外部契约缺失仍需提问。非行为改动按实际验证需要选方法 |
| `diagnosing-bugs` | 针对原症状的可运行失败信号、最小复现、可证伪假设、根因和回归 | 简单已定位缺陷按证据缩短诊断，不为凑数生成假设；复杂或不稳定问题保留完整调查纪律 |
| `code-review` | Standards/Spec 两轴、新上下文、真实 diff 与要求逐项比对 | 主代理提供基准、任务简报、完整变更包和标准；不重问这些已有信息，不因没有 tracker 阻断。使用 finish 协议覆盖未提交/未跟踪文件，不能只审 `...HEAD` |
| `pr` | 清楚解释行为、前后证据、实际影响与回退代价 | 项目模板与任务规模优先；它只指导 PR 正文，创建和合并授权由交付协议判断 |

普通调查直接使用代码、运行结果和一手资料；只有值得委派的独立研究才加载上游 `research`。原型、领域建模、架构方法也按它们实际解决的问题触发。

## 宿主能力

共享 Markdown 定义流程，不绑定特定模型名。Codex 用其原生文件、执行与子代理能力；Claude Code 用当前会话可用的原生对应能力。委派前检查实际可用工具，不把 Cursor 的 `/loop`、cloud agent 或 Project store 当作这两个宿主已有的 API。

使用独立子代理进行审查。实现者不兼任独立审查者；可并行则将 Standards 和 Spec 分开，资源受限则用独立的新上下文串行审查。没有独立上下文时只能交付“自审，独立审查待完成”，不能宣称达到了默认 ready PR 标准。

进程退出后的自动恢复、常驻队列与自动接单需要额外运行时，本 skill 只提供当前任务的推进与可人工接续的记录。
