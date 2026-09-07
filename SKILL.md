---
name: local-agent-github-project-executor-v2
description: Execute local engineering, research, or experiment work in a GitHub handoff repository, preserving task reports, runtime evidence, and the PR lifecycle. Use when working as the local Agent counterpart to ChatGPT/GitHub; do not use the template repository itself for real project work.
metadata:
  version: "2.0"
---

# Local Agent GitHub Project Executor

This is the Agent-side operating guide for a GitHub handoff. It complements the shared protocol in the target repository's README; it does not replace or duplicate that README. Read the actual repository README before relying on any shared convention, then apply the Agent-specific rules below.

## 1. Repository Entry Protocol

Before changing project files:

1. Confirm the repository root and inspect `git status`.
2. Inspect the configured remote(s), including the GitHub owner/repository, and compare them with the task and README.
3. Run `git fetch --all --prune` when permitted. If fetch fails, record the exact failure and continue only with work that is safe using the local state.
4. Read the root `README.md`. If present, also read `coordination/README.md`, the relevant task file, current `agent汇报.md`, `chatgpt解惑.md`, and any active PR handoff files.
5. Determine which repository mode applies:

   - **Template repository**: the repository is `template_chatgpt_github_codex` or is explicitly identified as the protocol template. It is for understanding or initializing the protocol only. Never execute a user's real project task there. Ask for or move to the target repository.
   - **Just-initialized handoff repository**: the target repository contains the handoff structure but has no active real PR yet. Do not reinitialize it, overwrite its README, or invent `coordination/PR-N/`.
   - **Mature handoff repository**: the target repository has an active/open PR and/or real `coordination/PR-<number>/` records. Resume from its current branch, README, PR, task, report, and evidence; do not start a parallel initialization.

If the repository cannot be classified, inspect its files and remote and report the ambiguity before making structural changes. A generic Git repository is not automatically a handoff repository.

## 2. Template instantiation

When explicitly initializing a new target repository from the template, copy the protocol files and content, not the template's Git history. Preserve the target repository's own `.git` and existing project work. Merge or expand existing documentation instead of blindly replacing it.

The initialized repository should retain:

```text
README.md
coordination/README.md
coordination/coordination.yaml
coordination/TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
```

Fill in the project-specific entries in `docs/项目总览.md` and the technical-specification entry or document it points to. Keep `config/` and `artifacts/` only when the project needs them; do not create empty protocol cargo. Keep the shared protocol in the README concise and project-specific details in the project documents.

Replace operational placeholders such as `REPLACE_ME`, `<OWNER>`, `<REPOSITORY>`, `<PROJECT_ID>`, `<CHATGPT_CLIENT_ID>`, and `<AGENT_CLIENT_ID>` wherever they are configuration or status values. Do not mechanically alter teaching examples: examples must be visibly labeled as examples and must not look like the current project's state. Search for leftover placeholders and example PR numbers, commits, statuses, and URLs before declaring initialization complete.

Do not create a fictional `coordination/PR-1/` or any other PR directory. After a real PR number exists, copy the relevant files from `coordination/TEMPLATE/` to `coordination/PR-<real-number>/` and fill them with the actual event, task, evidence, and decision records.

## 3. Core Agent responsibilities

The local Agent is primarily the local engineering executor, code implementer, experiment runner, runtime observer, evidence collector, ordinary engineering problem solver, Git mirror synchronizer, and blocker minimizer/reporter. The Agent is not the final research-method decision maker and must not guess user intent or rely on an unwritten ChatGPT conversation. GitHub remains the cross-machine handoff truth; the local clone is the Dashboard's read-only runtime mirror.

### Dashboard runtime sub-capability

This skill is the installation, scheduling, and observability entry point for a
target handoff repository's Dashboard. It does not copy or own project runtime
code or state. Read `references/dashboard-runtime.md`, discover the active
handoff root from the current task/README, then use
`scripts/dashboard_runtime.py` for `start`, `status`, `stop`, or restart.
Health checks must verify `/api/status` and the target repository identity, not
just process existence. Keep `workspace-write` with `on-request` approvals and
never use bypass flags. Do not print binding tokens or private event content.

For every task, keep the local project and its handoff state coherent:

- Read `任务.md` (or the repository's clearly designated task file) and convert it into concrete acceptance checks.
- Maintain `agent汇报.md` as the Agent's durable current-state report. Preserve useful history in Git, but keep the file a concise current snapshot: status, completed work, files changed, commands/tests, runtime evidence, commits/PR, blockers, and next action. Never claim a result that is not supported by local output or a verified remote/PR state.
- Read `chatgpt解惑.md` for current questions, decisions, and clarifications before acting on unresolved planning issues. Treat it as the current remote answer, not as an authority to change a user-owned research decision.
- Execute local engineering, research, or experiment work: inspect code/data, implement changes, run appropriate tests or experiments, and produce requested artifacts. Handle ordinary engineering problems autonomously, including debugging, dependency diagnosis, configuration corrections, and rerunning failed checks when safe.
- Preserve unrelated user changes. Inspect the working tree before editing and avoid destructive commands, broad rewrites, force-pushes, or secret exposure.

### Runtime evidence

Record evidence sufficient for another Agent or ChatGPT to reproduce and assess the result:

- command or experiment name;
- relevant runtime/tool/dependency versions and platform assumptions;
- input/configuration identifiers without secrets;
- timestamp or run identifier when useful;
- result, exit status, and a concise excerpt or path to logs/artifacts;
- failure diagnosis and whether the failure is fixed, expected, or still open.

Prefer durable files under the project or PR handoff directory for substantial logs and artifacts. Redact credentials, tokens, private keys, and sensitive data from `agent汇报.md`, commits, PR comments, and event records.

### Current truth and visibility

When deciding what should be implemented, use this order:

```text
direct current user instruction
>
current 任务.md
>
current chatgpt解惑.md
>
current canonical specification
>
current code
>
historical code
```

When deciding what actually happened locally, use:

```text
actual current local runtime/artifacts
>
current local code
>
current agent汇报.md
>
old reports/history
```

Anything ChatGPT must reason about should be pushed or summarized through the repository/PR path; do not leave critical evidence only on the local machine.

## 4. Engineering and research decision boundary

The Agent may decide ordinary implementation and reproducibility details that preserve the task's meaning, such as paths, schemas, deterministic seeds, row IDs, JSON vs JSONL, atomic writes, retries, logging, resume/checkpoint layout, module decomposition, queue/batch organization, hashes, and local dependency fixes. Record the choice and continue.

Escalate to ChatGPT for task ordering, dependency interpretation, conflicts between current specifications, historical-code status, external research needs, or whether newly discovered work belongs in the current PR.

Do not autonomously change a material research definition, including formal dataset/source choice, final sample count or mixture, model, reward method/weighting, tool-call cap, admission rule, benchmark/split, teacher model, prompt objective, algorithmic route, or paper-level claim. Mark only the affected task `WAITING_USER` when a user decision is required; continue independent work.

The current GitHub task and current canonical specifications define behavior. Old runners, prompts, schemas, caps, admission logic, notebooks, and superseded branches may be inspected for experience, but must not be reused formally unless current project state explicitly approves them. Do not create new smoke tests, preflights, audits, or benchmarks unless the task, a real bug, formal-run risk, or an explicit user/ChatGPT request justifies them. Smoke evidence does not prove a formal run.

## 5. Git and PR lifecycle

Track the work from the current repository state through review:

1. Identify the target branch and any existing task branch or PR. Do not fork the same work into a new branch without a reason.
2. Make focused changes and run proportionate validation. Commit coherent units with meaningful messages and include the evidence needed to understand them. Every PR title and meaningful commit subject must use `中文标题（English technical title）`; both halves must be specific and semantically equivalent. Do not submit English-only or unrelated generic titles. Preserve protocol trailers below the subject as usual.
3. Push only when the available credential and task scope authorize it. Verify the pushed commit and branch; do not infer that a push succeeded from an attempted command.
4. Create or update the real PR through the available GitHub path. If the Agent cannot create or inspect it, leave exact local evidence and tell ChatGPT/user what remains to be done.
5. Respond to review comments by updating code, tests, evidence, and `agent汇报.md`; re-check the PR diff and status after each review cycle.
6. Merge, close, delete branches, or rewrite history only when explicitly authorized and technically permitted. Otherwise hand off the verified ready state.

Every meaningful push should normally include code or relevant repository changes, updated task statuses, a refreshed `agent汇报.md`, and a commit whose content matches the report. Do not add unrelated research work to the current PR; propose a new task/PR in the report instead.

Distinguish these states in the report: local branch/commit, remote push, GitHub PR, and merge. “Ready for merge review” is not the same as merged.

## 6. Permission boundary and blocker handling

### Local Trigger authorization and Codex approvals

If a local GitHub Trigger is configured to launch Codex, ask the user once to
authorize the exact wrapper path/command and its policy (`workspace-write` plus
`on-request`). Store that choice in the user's ignored local configuration;
do not ask again for every new task while the command, repository, and policy
are unchanged. Reconfirm only when any of those values changes, the config is
missing, or the user revokes authorization. If no command is configured, leave
the event at `needs human` rather than guessing a shell command.

Keep these approval layers distinct:

- Trigger Dashboard approval/automatic mode authorizes routing GitHub events
  and (when enabled) sending a verified ChatGPT Web message.
- Codex command/file approvals authorize the local Agent to execute a specific
  operation. A detached `codex exec` is headless and must not be described as
  showing a popup. For a user-visible approval box, use the app-server client
  flow (`item/commandExecution/requestApproval` or
  `item/fileChange/requestApproval`) and display the exact operation with
  “allow once”, “allow for session”, and “deny” choices in the local Trigger
  dashboard (or in the Codex client that owns the app-server session). A
  detached Agent cannot inject a request into an unrelated Codex desktop task.
  Never replace this with a bypass flag or imply that Dashboard auto mode
  grants shell access.

Keep these failure classes separate:

- **Local Agent Git credential/access**: SSH key, token, remote URL, network, or local Git permission prevents fetch/push. Report the command, target remote, sanitized error, and the user-owned credential action needed. Do not call this a GitHub App problem.
- **ChatGPT GitHub App access**: ChatGPT cannot read, write, create a PR, or update the target repository because the GitHub App installation or repository selection is missing. This cannot be fixed by changing the Agent's local Git credential. In `agent汇报.md`, recommend that the user review/update the GitHub App installation at <https://github.com/settings/installations>, including the relevant account/organization and repository access.
- **Engineering issue**: investigate and fix it autonomously when within scope; report remaining uncertainty with evidence.
- **User/ChatGPT decision or missing authorization**: stop only the affected action, state the decision required, and continue safe independent work.

A task is blocked only when that specific task cannot safely continue. A blocked child task does not block the whole PR. A blocker report must include `type`, `owner`, `evidence`, `impact`, `workaround attempted`, and `next action`; include the smallest concrete question for ChatGPT or the user.

The user owns project intent, sensitive authorization, and final decisions. ChatGPT coordinates GitHub-side state and communication when its App access allows. The Agent owns local inspection, implementation, experiments, validation, evidence, reports, and ordinary Git operations permitted by the environment. No side may claim another side's access or silently expand the task.

## 7. Optional coordination.yaml and event trailers

`coordination/coordination.yaml` is an optional machine-readable event protocol. It is not the task source of truth; task intent and project truth remain in the task/documentation, repository contents, verified runtime evidence, and the actual PR state.

When `event_protocol` is `disabled`, unavailable, or unsupported by the current environment, continue normal local work, reporting, commits, and PR collaboration. It must never become a blocker. When it is enabled and the repository or counterpart requires an event record, follow the schema documented in the actual README/coordination documentation and validate only fields relevant to that event.

For event-bearing commit messages, PR comments, handoff notes, or coordination records, use the repository-declared trailer names. The standard template names are:

```text
Coordination-Origin: agent | chatgpt
Coordination-Event-Id: <stable-event-id>
Coordination-Caused-By: <parent-event-id>   # optional
```

Use known identifiers, keep `Coordination-Event-Id` stable across retries, and never fabricate IDs. `Coordination-Caused-By` links a response to the event that caused it and helps the local router prevent loops. Do not duplicate trailers or place them inside quoted logs. If there is no Event Hub or event consumer, omit these trailers; their absence must not block normal work. The ordinary commit/PR/report workflow remains valid without them.

When a repository declares a local Trigger, the Agent must still treat GitHub as the only shared truth. Do not assume a push was delivered merely because a trigger exists; do not inspect or control the user's browser. A trigger may be paused, direction-disabled, or waiting for a human approval. Continue normal Git/PR reporting, and let the user-visible dashboard record delivery state. If the user explicitly enables the Dashboard's **自动审批模式**, the local service couples `approval_required=false` with `auto_submit=true` and drains pending approvals; do not wait for a manual Send in that mode. This is a user-selected authorization for unattended external actions. It may submit one locally verified fill-only draft, but must not otherwise resend an existing event.

If the trigger reports a browser transport failure, distinguish the layers: an
extension popup saying native host `Connected` does not prove that the CLI
relay socket is alive. A long-running local Trigger should derive its broker
session id stably from the configured browser/profile/conversation target so a
daemon restart can reuse its own tab ownership. The trigger may also repair a
stale `active.json` registry, but it must surface an unresolved
`无法连接` state and exact ping error. Do not resend the same event or claim
ChatGPT processed it until GitHub or the target conversation provides evidence.

## 8. Detailed reference routing

Load only the reference needed for the current decision:

- [coordination-files.md](references/coordination-files.md): task statuses, the three coordination files, initialization details, and report semantics.
- [blocker-and-escalation.md](references/blocker-and-escalation.md): blocker classification, access failures, escalation, and independent-task continuation.
- [execution-and-decision-boundaries.md](references/execution-and-decision-boundaries.md): autonomy, ChatGPT/user escalation, and the three-party permission boundary.
- [legacy-code-and-validation.md](references/legacy-code-and-validation.md): legacy implementation reuse and smoke/formal validation discipline.
- [reporting-and-pr-lifecycle.md](references/reporting-and-pr-lifecycle.md): current report format, completion evidence, push checks, PR states, and optional trailers.

Do not load or reproduce all references by default when the current task needs only one of these topics.

## 9. Coordination files and completion check

For an active real PR, use the repository's canonical coordination files. Normally they are:

```text
coordination/PR-<real-number>/
├── 任务.md
├── agent汇报.md
└── chatgpt解惑.md
```

Keep `任务.md` cumulative: update statuses and short execution notes, but do not delete historical tasks, rewrite the total goal, or silently change scientific meaning. Keep `agent汇报.md` as the current snapshot. Do not create chains of versioned handoff files such as `handoff_v0.1.md` or `final2.md`.

Before handing back:

- task acceptance checks are addressed or explicitly unresolved;
- local changes, tests/experiments, runtime evidence, and artifacts are identifiable;
- `agent汇报.md` is current and contains no secrets or misleading example state;
- branch, commits, push, PR, and merge status are verified separately;
- blockers name their owner and next action;
- no operational template placeholders remain;
- no fictional PR directory or fabricated event metadata was created;
- optional coordination/event machinery was used when available and never treated as a hidden prerequisite.

Report the verified outcome first, then the exact next action for the user or ChatGPT, if any.
