# mattpocock/skills 的 Skill 质量测试调查

研究日期：2026-11-16。问题：[`mattpocock/skills`](https://github.com/mattpocock/skills) 这个仓库**实际上**如何做 Skill 的质量测试。只使用一手资料：默认分支 `main` 的 README、CONTRIBUTING、package.json、测试/eval 配置与脚本、fixtures、CI workflows，以及仓库明确引用且实际使用过的官方工具命令。不根据 Skill 内容或常见实践推测，没有执行任何下载的脚本。

调查方式：`gh api`/`gh search code` 只读访问远程仓库，全部来源固定到 `main` 分支 HEAD **`5863806dd4e15c63174bee4e7515a4256792ecfa`**（推送时间 2026-11-13T12:30:31Z）。逐项枚举了该提交的完整 git tree，确认仓库级文件全集；对全文做过 GitHub code search 交叉验证（hooks、test、validate 等关键词）。分支保护和 rulesets 属于 GitHub 侧配置而非分支内文件，已用 API 尝试读取并单独标注。

## 结论速览

| 问题 | 结论 | 性质 |
| --- | --- | --- |
| 1) 静态校验/lint/frontmatter 检查 | **有，但只有两个，且都不在 CI**：`claude plugin validate . --strict`（只校验 plugin manifest，人工在改 manifest 后运行）；`check-plugin-version`（校验 package.json 与 plugin.json 版本一致，有 npm script 但没有任何 workflow 调用）。其余结构约定（README/plugin.json/docs/ask-matt 同步、frontmatter 与 openai.yaml 配对、禁用 em-dash）只是 CLAUDE.md 里的成文规则，靠维护者自己的 agent 执行，无任何自动化检查器 | 人工/本地，非 CI |
| 2) 行为 eval/对照实验/触发测试/人工评审 | **没有任何行为 eval、对照实验、触发测试、fixtures 或评分器**。质量信号是人工的：issue 准入门槛（必须真实会话观察到的失败）、结构化 bug 模板（harness/模型/版本/repro）、维护者本人做手动端到端安装冒烟并记录在 ADR 里；PR 仅协作者可开，等于人工 review 是默认关卡 | 人工评审为主 |
| 3) 测试如何运行、如何判分、CI | **没有测试可运行，也没有判分**。CI 共 3 个 workflow：release（只做 changesets 版本 PR）、needs-info（14 天无回复自动关 issue）、triage-label（给新 issue 加标签），无一运行测试或 lint。不存在能产生 check run 的工作流，因此从仓库证据看也不存在任何必需的 CI 质量门 | 无测试、无判分、无质量门 |
| 4) 没做/无法确认的常见质量测试 | 缺：frontmatter schema 校验、YAML lint、markdown 链接检查、em-dash 规则的工具化、行为 eval、触发精度测试、golden transcript、LLM 评判、fixture 仓库、脚本单测、pre-commit hooks、CI 测试任务、dependabot。无法从仓库确认：分支保护/必需 review 设置（API 对非管理员返回 404，rulesets 为空） | 见下文清单 |
| 5) 对自己 skills 仓库的可复用做法 | 成文的结构不变量、版本同步脚本、manifest 校验命令、changesets 管理提示词版本、严格的 issue 门槛 + 结构化模板、beta 桶作为反馈回路、`.out-of-scope/` 决策记录；以及它的**空白清单**本身就是一份低成本的补强 adoption 列表 | 见下文 |

## 1) 静态校验 / lint / frontmatter 检查

### 1.1 仓库里真实存在的两个检查

**a. `claude plugin validate . --strict`（官方 Claude Code 插件校验）。** CLAUDE.md 指示"改动任一 manifest 后运行它"，并说明 ADR 0002 记录了原因：

- 来源：[`CLAUDE.md` L11](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L11)（"Run `claude plugin validate . --strict` after touching either manifest"）。
- 实际使用过的证据：ADR 0002 记录了端到端验证结论"`claude plugin validate . --strict` passes"，以及 2026-08-05 在 Claude Code 2.1.222 上对官方 marketplace 实装的核实（install/details 能解析全部 promoted 技能）：[`.agents/adr/0002-ship-as-a-claude-code-plugin.md` L11](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/adr/0002-ship-as-a-claude-code-plugin.md#L11)、[L36-L40](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/adr/0002-ship-as-a-claude-code-plugin.md#L36-L40)。
- **但它是人工步骤**：全文 code search 显示该命令只出现在 `CLAUDE.md` 和 ADR 0002 两处，**没有任何 workflow 或脚本调用它**。它校验的对象是 `.claude-plugin/plugin.json` / `marketplace.json` 两个 manifest 的结构与一致性，不是逐 SKILL.md 的 frontmatter 规则。

**b. 版本一致性检查 `check-plugin-version`。** `scripts/sync-plugin-version.mjs` 把 package.json 的 version 同步进 `.claude-plugin/plugin.json`，带 `--check` 时只校验不改写、不一致则 exit 1：

- 来源：[`package.json` L11-L15](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/package.json#L11-L15)（三个 script 中唯一的 check）、[`scripts/sync-plugin-version.mjs` L17-L27](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/scripts/sync-plugin-version.mjs#L17-L27)。
- 约束写成了 ADR 不变量："plugin.json 的 version 跟随 package.json，发布时一起 bump"，且 `npm run version` 会在 changesets 之后自动跑同步脚本：[`0002-ship-as-a-claude-code-plugin.md` L28](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/adr/0002-ship-as-a-claude-code-plugin.md#L28)、[L53](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/adr/0002-ship-as-a-claude-code-plugin.md#L53)。
- **注意**：code search 显示 `check-plugin-version` 只被 package.json 自己引用，**没有任何 workflow、hook 或文档流程调用它**；release workflow 里跑的是不带 `--check` 的 `npm run version`（见 §3）。

### 1.2 成文的结构约定（无自动化检查器，靠 CLAUDE.md 驱动维护者的 agent 执行）

以下规则全部写进 `CLAUDE.md`/`AGENTS.md`（两份内容相同），但没有找到任何脚本、workflow 或 hook 去强制它们：

- promoted 桶（`engineering/`、`productivity/`）的每个技能必须同时出现在顶层 README 和 `.claude-plugin/plugin.json` 的 `skills` 数组，其余桶禁止出现：[`CLAUDE.md` L9](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L9)。
- promoted 技能必须有镜像的 docs 页 `docs/<bucket>/<skill>.md`，行为变更时 re-sync：[`CLAUDE.md` L17](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L17)、模板见 [`.agents/writing-docs.md`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/writing-docs.md)。
- `ask-matt` 路由图必须与技能集合保持同步：[`CLAUDE.md` L21](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L21)。
- 每个 SKILL.md 要么是 user-invoked（frontmatter `disable-model-invocation: true` + `agents/openai.yaml` 里 `policy.allow_implicit_invocation: false`），要么是 model-invoked，且"两个 harness 要么都是 user-invoked 要么都不是，保持同步"：[`CLAUDE.md` L19](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L19)、[`.agents/invocation.md` L10](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/invocation.md#L10)。这是**最接近 frontmatter 检查的规则，但没有工具 enforcement**。
- 全仓散文禁用 em-dash：[`CLAUDE.md` L25](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L25)。code search 未发现任何脚本检查它，属于纯约定。

### 1.3 否定性证据（用什么证明"没有更多 lint"）

- [`package.json`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/package.json) 全文 21 行：scripts 只有 changeset/version/check-plugin-version，devDependencies 只有 `@changesets/changelog-github` 和 `@changesets/cli`（发布管理工具，非测试/lint）。**没有任何 eslint/prettier/yaml/frontmatter 类依赖。**
- 完整 git tree 枚举：仓库级脚本只有 `scripts/link-skills.sh`（开发者本地软链安装器）、`scripts/list-skills.sh`（列出 SKILL.md）、`scripts/sync-plugin-version.mjs` 三个，[tree 快照](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa)。
- code search 在整个仓库中搜 pre-commit/husky/lefthook：**0 命中**；`test` 关键词在 package.json 中：0 命中。

## 2) 行为 eval、对照实验、触发测试、人工评审

### 2.1 没有任何自动化行为测试（否定性结论，有完整枚举支撑）

- 完整 tree 中不存在任何 `test/`、`fixtures/`、`eval*.json`、golden transcript、评分器配置文件；`skills/` 下的脚本（如 `wizard/template.sh`、`diagnosing-bugs/scripts/hitl-loop.template.sh`、`misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh`）都是**技能交付给用户的内容**，不是对技能自身的测试。`skills/engineering/tdd/tests.md`、`mocking.md` 是给用户项目的测试写作指南，同样不是本仓的测试。
- package.json 无 test script、无任何测试框架依赖（§1.3）。
- 因此：**无行为 eval、无对照实验、无触发精度测试、无 LLM 评判、无 fixtures**。技能质量不经过任何自动化行为验证就发布。

### 2.2 质量信号来自人工评审与真实使用反馈

- **PR 仅协作者可开**，外部贡献者只能提 issue，由维护者本人实现：[`CONTRIBUTING.md` L15](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CONTRIBUTING.md#L15)（"Pull requests are open to collaborators only, so describe the fix in an issue instead."）。即默认的质量门是维护者的人工判断，而不是 CI。
- **issue 准入门槛**：只收"真实会话中观察到的失败"（observed failure），且必须符合仓库理念：[`SCOPE.md` L7-L12](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/SCOPE.md#L7-L12)。这是对"变更是否值得做"的人工质量判断，不是对 skill 正确性的测试。
- **结构化 bug 模板**强制收集 skill 名、版本/commit、harness 及版本、模型及 effort、最小复现步骤、预期行为（含指出 SKILL.md 哪一行）：[`.github/ISSUE_TEMPLATE/bug.yml` L1-L8](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.github/ISSUE_TEMPLATE/bug.yml#L1-L8)（后续字段要求 version/harness/model/repro 均为 required）。这使人工 triage 有据可依，也是全仓唯一的"回归信号"来源。
- **手动端到端冒烟**：ADR 0002 记录维护者在 Claude Code 2.1.222、Codex 0.161.0、Copilot CLI 上人工验证过 install/解析行为（[L36-L40](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/adr/0002-ship-as-a-claude-code-plugin.md#L36-L40)、[L55-L58](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.agents/adr/0002-ship-as-a-claude-code-plugin.md#L55-L58)）。这是人工 smoke test，不自动复跑。
- **beta 桶即反馈回路**：`in-progress/` 公开征求意见，不进正式 plugin：[`CLAUDE.md` L4-L8](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CLAUDE.md#L4-L8)。新技能先在这里经真实使用打磨。
- **明确拒绝做自动 verify**：`.out-of-scope/setup-skill-verify-mode.md` 记录了一个 verify/check mode 的功能请求（#106）被正式拒绝，理由是 setup 技能是 prompt-driven，让维护者用自然语言要求"只校验不写"即可，不维护第二条代码路径：[`.out-of-scope/setup-skill-verify-mode.md`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.out-of-scope/setup-skill-verify-mode.md)。这是仓库对"要不要加测试型功能"的明确立场证据。

## 3) 测试如何运行、如何判分、是否有 CI

### 3.1 没有测试可运行、没有判分

§1.3 和 §2.1 的枚举结论：不存在测试目标、测试命令、判分器或覆盖率概念。`npm run` 可用的命令只有 changeset 相关三条。

### 3.2 CI 实况：3 个 workflow，0 个质量检查

`.github/workflows/` 全集（[目录](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa/.github/workflows)）：

| Workflow | 触发 | 做什么 | 来源 |
| --- | --- | --- | --- |
| `release.yml` | push 到 main | checkout → setup-node 22 → `npm ci` → changesets/action 创建版本 PR 并打 tag。**无 test/lint 步骤**；`npm ci` 只安装 changesets 两个依赖 | [`release.yml` L17-L37](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.github/workflows/release.yml#L17-L37) |
| `needs-info.yml` | 定时 + 手动 | 对 14 天无回复的 `needs-info` issue 自动关闭（actions/stale） | [`needs-info.yml`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.github/workflows/needs-info.yml) |
| `triage-label.yml` | issue opened | 给新 issue 加 `needs-triage` 标签 | [`triage-label.yml`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.github/workflows/triage-label.yml) |

发布流程的质量相关动作只剩一件：`npm run version` 在 changesets 之后自动同步 plugin.json 版本（release.yml L32 调用），防止版本漂移。

### 3.3 无法确认项：分支保护

`GET /repos/mattpocock/skills/branches/main/protection` 对非管理员返回 404，`/rulesets` 返回 `[]`。对公共仓库无 admin 权限时 404 既可能是"未配置"也可能是"不可见"，**无法从此处区分**；但 §3.2 已证明没有任何 workflow 会产生 check run，因此即使存在分支保护，从仓库证据看也不存在"必需通过的 CI 检查"。

## 4) 没做、或无法从仓库证据确认的常见质量测试

**明确没有做（有枚举/搜索支撑）：**

1. SKILL.md frontmatter 的 schema 校验（name/description 长度、必填字段、unknown 字段）——无工具。
2. `agents/openai.yaml` 的 YAML 语法 lint 及与 frontmatter 的配对检查（`disable-model-invocation` ↔ `allow_implicit_invocation`）——规则成文，无 enforcement（§1.2）。
3. Markdown 链接有效性检查（README、docs 页里大量相对链接指向 SKILL.md）。
4. em-dash 禁令的工具化（§1.2）。
5. 行为 eval / 触发测试 / golden transcript / 对照实验 / LLM 评判 / 人工评审 rubric 打分（§2.1）。
6. 仓库自带脚本的单测（`sync-plugin-version.mjs` 等无测试）。
7. pre-commit / pre-push hooks（code search 0 命中）。
8. CI 中的任何 test/lint job（§3.2）。
9. dependabot 等依赖更新配置（`.github/` 下只有 ISSUE_TEMPLATE 和 workflows）。
10. `check-plugin-version` 未接入 CI（§1.1b）。

**无法确认（需要 GitHub 设置页或管理员权限，超出分支内一手资料）：**

- 分支保护、必需 approving review、必需签名提交等合并门槛（§3.3）。
- 维护者本机是否有未入库的私人检查（从仓库证据不可知；link-skills.sh 自述是 dev-only，非 installer，见 [scripts/link-skills.sh](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/scripts/link-skills.sh)）。

**有意不做（有决策记录，区别于"疏忽"）：**

- 不给 setup 技能加 verify/check mode（§2.2 末条）。
- `misc/` 桶整体冻结，不修任何 issue（[SCOPE.md L17](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/SCOPE.md#L17)）。

## 5) 对用户自己 skills 仓库的可复用做法

### 5.1 可直接照搬的做法

1. **成文的结构不变量放进 AGENTS.md/CLAUDE.md**（让维护 agent 在每次改动时自查）：promoted 集合 == 顶层 README 条目 == plugin.json `skills` 数组；docs 树镜像；路由器文档与技能集合同步；frontmatter 与 openai.yaml 双 harness 配对。来源：CLAUDE.md L9/L17/L19/L21。
2. **版本同步脚本 + 发布时强制**：一个小 mjs 在 `npm run version` 里把 package.json 版本写进 plugin.json，另提供 `--check` 供本地/CI 校验；并把"version 必须一致"写进 ADR。来源：sync-plugin-version.mjs、ADR 0002 L28/L53。
3. **manifest 改动后跑 `claude plugin validate . --strict`**（Claude Code 官方命令；本调查中未越出仓库引用它的证据去引外部文档）。把结果连同 install 冒烟一起记进 ADR。来源：CLAUDE.md L11、ADR 0002。
4. **用 changesets 管理提示词版本**：每次技能行为变更附 changeset，生成带 PR/issue 链接的 CHANGELOG，让"提示词 regress/修复"有版本史可查。来源：package.json L11-L19、[CHANGELOG.md](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/CHANGELOG.md)、[.changeset/config.json](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/.changeset/config.json)。
5. **严格的 issue 门槛 + 结构化 bug 模板**：只收真实会话失败，模板强制 harness/模型/版本/最小复现/预期行为（最好指出 SKILL.md 行号）。来源：SCOPE.md L7-L12、bug.yml。
6. **beta 桶 + 拒绝清单**：`in-progress/` 公开收集真实使用反馈；`.out-of-scope/` 把拒绝过的东西和理由写成文件，防止重复讨论。来源：CLAUDE.md L4-L8、SCOPE.md L20-L28、`.out-of-scope/` 目录。
7. **协作者限定 PR**：如果不想维护测试基建，把合并权收到自己手里、用 issue 驱动，是该仓库实际采用且证据充分的模式。代价完全转给维护者本人。来源：CONTRIBUTING.md L15。

### 5.2 该仓库没做、而我们低成本就能补强的（差距即清单）

以下每项在上游均为空白，对个人 skills 仓库实现成本很低：

- 把 `claude plugin validate . --strict` 和 `check-plugin-version` 接进一个 CI workflow（上游最大的可抄作业漏洞：两个检查都已存在却都不在 CI）。
- 一个 20 行的 frontmatter/openai.yaml 一致性 lint（校验 name/description 存在、user-invoked 双文件配对、YAML 可解析）。
- markdown 链接检查（它 README 与 docs 全靠相对链接）。
- 如果对质量有更高要求：对 2-3 个核心 skill 建最小 golden-session eval（固定输入+期望行为断言），上游完全没有这层，做了就是差异化。

## 复核方法与来源

- 工具：`gh api`（contents/git trees/search code）只读访问；未 clone、未执行仓库内任何脚本；未登录 Claude CLI 运行 validate。
- 快照：全部 blob 链接固定在 commit `5863806dd4e15c63174bee4e7515a4256792ecfa`。
- 完整性论证：枚举了该 commit 的全部非 `skills/` 文件与全部 workflow；对 hooks/test/validate 关键词做了全仓 code search；`.github/` 目录只有 ISSUE_TEMPLATE 与 workflows 两个子项。
- 已知边界：分支保护不可见（§3.3）；无法观察维护者本机流程；本报告没有运行 `claude plugin validate`，其具体校验范围以仓库自身记录（"passes"、manifest 结构问题在 ADR 中的讨论）为限。
