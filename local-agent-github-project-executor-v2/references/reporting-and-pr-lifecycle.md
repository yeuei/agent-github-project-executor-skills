# Reporting and PR Lifecycle

The actual target repository README is the shared-protocol entry point. This reference supplies Agent-specific reporting and PR details; do not copy the template README wholesale into the report.

## 1. Current report

`agent汇报.md` is a current snapshot, not a historical notebook.

Overwrite it after meaningful work.

Include enough information for ChatGPT to reason without local access.

---

## 2. Compact reporting is preferred

Good:

```markdown
# Agent 当前汇报

## 当前
PR #8
branch: ...
commit: ...

## 正在执行
T8.2 Tool-Star 全量转换

processed: 31,240 / 53,971
canonical: 23,181
accepted: 21,904
rejected: 1,277

## ReTool
1000/1000 processed
accepted: 963

## 当前 blocker
Search-R1 has two materially different source files.

## 不受影响任务
Tool-Star continues.
ReTool is done.

## 需要 ChatGPT
Only decide whether Search-R1 source choice is mine, ChatGPT's, or the user's.
```

Do not write dozens of pages of historical handoff.

---

## 3. Task completion evidence

Mark a child task done only when the task's actual acceptance condition is met.

Examples:

- code implementation task: code exists and relevant check/run succeeded;
- conversion task: intended input was processed and outputs/statistics exist;
- formal experiment task: formal run actually completed;
- benchmark task: required evaluation actually ran.

Do not use:

- plan-only evidence;
- file-existence-only evidence;
- smoke-only evidence;

for a stronger completion claim.

---

## 4. Total task completion

Before marking the PR total task done:

1. no required TODO remains;
2. no required BLOCKED remains;
3. no required WAITING_USER remains;
4. all active required tasks are done;
5. runtime/code evidence matches the statuses.

Then update the total task to done and report:

> 当前 PR 已达到业务完成条件。

This means ready for merge review, not automatic merge.

---

## 5. PR scope

Do not add unrelated work just because you discovered it.

Report:

> 建议新增独立任务/PR：...

Let ChatGPT decide.

---

## 6. Document cleanup

Do not create:

- `handoff_v0.1.md`;
- `handoff_v0.2.md`;
- `final2.md`;
- `latest.md`.

Update canonical documents in place.

When a new canonical file supersedes an old one, remove the old one when safe.

Git history is the archive.

---

## 7. Push checklist

Before a meaningful push:

- implementation is internally consistent;
- task statuses reflect reality;
- `agent汇报.md` reflects the same commit/state;
- no secrets are added;
- no unnecessary run caches or huge artifacts are included;
- obsolete coordination versions are not added.

## 8. Verify lifecycle states separately

Report these independently:

```text
local branch/commit → remote push → GitHub PR → review state → merge state
```

An attempted push is not a verified push, and “ready for merge review” is not merged. If ChatGPT cannot access the repository through its GitHub App, record that separately from local Git access and recommend <https://github.com/settings/installations>.

## 9. Optional event trailers

When the repository/counterpart uses event-bearing messages, optional final-line trailers are:

```text
Origin: <source-system>/<source-id>
Event: <event-id>
Dedup: <stable-deduplication-key>
```

Use known IDs and a stable deduplication key; never fabricate or duplicate them. Without an Event Hub or event consumer, omit the trailers and continue normally. Missing trailers or a disabled `event_protocol` must not block work.

