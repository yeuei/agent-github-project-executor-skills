# Coordination Files Protocol for the Local Agent

Use this reference after the target repository has passed the Repository Entry Protocol in `SKILL.md`. The target repository's actual root README and `coordination/README.md` remain the shared-protocol authority; this file defines Agent-specific handling.

## 0. Repository and initialization rules

Never perform a real project task in `template_chatgpt_github_codex`. For a new target repository, preserve or expand the existing README and retain:

```text
README.md
coordination/README.md
coordination/coordination.yaml
coordination/TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
```

Do not copy the template Git history. Fill `docs/项目总览.md` and the technical-specification entry as applicable; keep `config/` and `artifacts/` only when the project needs them. Replace operational placeholders (`REPLACE_ME`, `<OWNER>`, `<REPOSITORY>`, `<PROJECT_ID>`, `<CHATGPT_CLIENT_ID>`, `<AGENT_CLIENT_ID>`), while leaving clearly labeled teaching examples intact. Do not create `coordination/PR-N/` until a real PR number exists; then copy from `coordination/TEMPLATE/` to `coordination/PR-<real-number>/`.

## 1. `任务.md`

This is the formal execution contract.

Always read it before starting work.

The first line is the PR total goal.

Example:

```markdown
# [ ] PR #8 总任务：完成 Stage1 Scheme1 正式数据构造与训练
```

Child tasks use:

```text
[ ] TODO
[~] RUNNING
[x] DONE
[!] BLOCKED
[?] WAITING_USER
[-] SUPERSEDED
```

### Agent permissions

You may:

- change task status based on actual execution;
- add short execution notes under existing tasks;
- mark a task blocked when it truly cannot continue;
- mark waiting-user when a genuine human decision is required.

You must not:

- add a new research goal on your own;
- rewrite the total goal;
- silently change the scientific meaning of a task;
- delete old task entries.

If you discover a missing task, propose it in `agent汇报.md`. ChatGPT decides whether to add it.

---

## 2. `agent汇报.md`

This is your current-state report to a remote coordinator that cannot see your machine.

Overwrite it on meaningful updates.

Recommended structure:

```markdown
# Agent 当前汇报

## 当前身份
- PR:
- branch:
- commit:
- 本地代码目录:

## 当前任务
- task:
- status:

## 本次完成
1.
2.

## 代码变化
- file:
- purpose:

## 本地输入
- dataset:
- model:
- config:
- manifest:

## 实际运行
command:
...

run directory:
...

## 当前结果
- processed:
- accepted:
- rejected:
- failures:
- tool calls:
- other metrics:

## 当前问题
...

## 已尝试
1.
2.

## 为什么无法继续自行决定
...

## 不受影响、仍可继续的任务
...

## 需要 ChatGPT 回答
<smallest concrete question>
```

### Minimum blocker context

When reporting a blocker, include:

1. current task;
2. current commit;
3. relevant local file(s);
4. input data/config;
5. code changed;
6. actual command;
7. actual output/error;
8. attempts already made;
9. why those attempts did not resolve it;
10. what you can still decide yourself;
11. what exact remote decision is needed;
12. which other tasks can continue.

---

## 3. `chatgpt解惑.md`

Read this before acting on unresolved planning issues.

Treat it as the current remote answer, not a historical transcript.

If it grants you authority to freeze an engineering choice, proceed and record the choice.

If it says a decision requires the user, do not substitute your own research choice.

---

## 4. Cumulative vs overwrite behavior

```text
任务.md
→ cumulative; do not delete historical task entries

agent汇报.md
→ current snapshot; overwrite

chatgpt解惑.md
→ current ChatGPT answer; ChatGPT overwrites
```

---

## 5. Meaningful push

A meaningful push should normally include:

- implementation or relevant repository change;
- task-status update;
- refreshed `agent汇报.md`;
- consistent commit metadata.

Do not create a new handoff file for every push.

