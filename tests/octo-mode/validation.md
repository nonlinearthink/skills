# octo-mode 初版验证

日期：2026-11-16。适配的 Matt 基线为 `5863806dd4e15c63174bee4e7515a4256792ecfa`，本次通过 GitHub API 核对仍为 main。`octo-mode` 保留上游工程方法，阶段协调与澄清策略使用本仓库的适配协议。

## 可重复的检查

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/octo-mode -v
python3 skills/octo-mode/scripts/resolve_matt.py --root <Matt源码目录> tdd code-review diagnosing-bugs
npx skills add ./skills --list
```

定位回归覆盖 flat install、上游 checkout、单技能路径、来源优先级、同名替代来源、符号链接去重、缺失、版本漂移和 CLI 无效输入。源文件哈希用于提示入口漂移，不证明支撑材料完全一致。

## 行为评测场景

在独立临时仓库中提供 Python 标准库缓存项目、已有测试、未提交的用户笔记和已固定的 Matt 方法路径。评测者只收到用户目标、skill 路径、仓库和允许操作范围，自行运行流程。临时仓库不含远端，禁止外部写入。

1. **只读调查：** “请调查缓存为什么在数据源暂时抛出 OSError 后，再查同一个 key 会直接返回 None；只解释原因和建议，不修改代码。” 检查是否调查真实路径、给出运行证据且保持仓库原样。
2. **缺陷修复：** “修复查询缓存：数据源暂时抛出 OSError 之后，同一个 key 第二次查询直接返回 None。目标是失败后还能重试，成功结果仍正常缓存。只做本地修改，不提交不创建 PR。” 检查失败/通过证据、行为回归、用户改动保留、独立审查及本地终点。

## 已执行结果

- Skill Creator 的 `quick_validate.py`：通过。使用临时 PyYAML 运行环境，未向项目增加依赖。
- `test_resolve_matt.py`：8 项通过，覆盖上面的定位契约。初次运行发现测试夹具未规范化 macOS 的 `/var` 别名，修正夹具后通过；定位脚本本身无需因此改动。
- 真实上游核对：9 个方法入口哈希及 4 个阶段来源路径与固定 checkout 相符。
- 首次 Skills CLI 验证（旧名）：发现 `dev` 等 4 项 skill；在独立临时目录用 `--skill dev -a codex claude-code -y --copy` 安装成功，分别生成 `.agents/skills/dev` 与 `.claude/skills/dev`。未安装到用户的全局目录或实际项目。
- 只读调查前向测试：通过。评测者自行选择并读取 `diagnosing-bugs`，在仓库外实际复现两次，并以异常类型对照定位原因；项目原有两项测试通过。主代理复核目标源码及测试无修改，只有预先存在的 `NOTES.md` 改动。
- 缺陷修复前向测试：通过。评测者自行加载诊断/TDD 方法，新增针对原症状的测试先得到两个失败 subcase；最小修复后 3 项 unittest 通过。两个 fresh-context 审查者串行完成 Standards/Spec，均为 0 findings，Spec 轴独立重跑测试通过；主代理复核代码哈希与两轴一致、原用户笔记保留且没有新提交或 PR。
- 入口独立审查：无实质发现。审查者只读检查全部新 skill、定位回归及 README 新增内容，并对照已确认范围和固定上游源文件；另行复跑 8 项定位回归、核验 9 个方法入口和许可一致性。

2026-11-17 命名变更：按用户选择统一改为 `octo-mode`，同步源码目录、元数据、测试路径、调用示例和文档。结构校验、8 项定位回归、Skills CLI 发现及本地链接检查均通过；工程流程未变，保留首次行为评测证据。

尚未评测的范围包括：Claude Code 原生运行、两个宿主的隐式触发精度、多单元 worktree 并发、真实远端 PR/CI/合并、进程重启后的自动恢复。后者不属于该 skill 的能力承诺。
