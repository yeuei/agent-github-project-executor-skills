# Dashboard runtime sub-capability

## Preconditions and discovery

Use the current handoff repository named by the active task and README. Resolve
that root, verify `trigger/trigger.py`, and derive local config/database paths
from the project (`trigger/config.local.json` and its documented DB default).
Never assume a fixed user path or copy runtime source into this skill.

Python 3 is required. Project-specific GitHub, browser, command, and ChatGPT
settings belong in ignored local configuration. Keep execution under
`workspace-write` and `on-request`; never use a bypass flag.

## Lifecycle

```text
python scripts/dashboard_runtime.py start --project-root /absolute/path/to/handoff
python scripts/dashboard_runtime.py status --project-root /absolute/path/to/handoff
python scripts/dashboard_runtime.py stop --project-root /absolute/path/to/handoff
```

`start` is idempotent and waits for the localhost endpoint. When the target
repository provides `trigger/codex-thread-monitor.py`, it also starts that
separate local monitor. `status` probes `/api/status`, reports reachability,
the recorded Dashboard process identity, and the recorded monitor PID; check
the returned repository path before acting. Restart means `stop`, `start`, then
`status`.

If the port is occupied, inspect the status payload and use an explicit
alternate `--port`; never kill an unknown process. On failure preserve the
`/tmp` log path and exact error. `stop` only terminates Dashboard and monitor
PIDs recorded by the launcher.

## Runtime/API boundary

The Dashboard observes the handoff project's event history, historical task
snapshots, and binding.v1 state through `/api/status`, event/task-history
endpoints, and `/api/bindings`. The handoff project remains the source of truth;
the skill only schedules and observes the runtime. Tokens, full conversation
URLs, and private payloads must not appear in output, logs, or reports.

## Local Git mirror policy

Dashboard 应从交接仓库的本地 Git 克隆读取 PR、commit、coordination 文件、事件状态和历史 `任务.md` 快照。克隆默认位于项目 `.cache/`（必须忽略）。启动时校验或创建克隆并同步一次；运行中只对已知分支做有界增量同步。网络不是正常渲染的前置条件；“从 GitHub 刷新”才执行显式网络同步或修复。失败时保留最后一次本地状态并显示准确错误。历史任务必须解析节点 commit SHA 中的 `coordination/PR-<N>/任务.md`；不存在则明确标记不可用，禁止用当前工作树任务文件替代。
