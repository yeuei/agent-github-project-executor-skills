# Persistent Codex-thread continuation

Use this route when a local Dashboard or another local event source should
continue a stable Codex Agent thread without relying on a scheduled task.
It is a local-only control path, not a way to inject into ChatGPT Web.

## Target selection

Use only a user-selected `kind=codex` thread from the same local Codex
installation, or create a dedicated thread with `ephemeral: false`. Persist the
chosen `thread_id` in ignored local state. A ChatGPT Web conversation ID is not
compatible with `thread/resume`. Do not target an unrelated active task; it can
race with the user's own input and produce misleading context.

The default route should create and reuse one dedicated local-agent thread.
Allow an explicit user choice to replace that target. Show the title, working
directory, and last-updated time before saving a selection.

## Monitor and signal contract

Keep the monitor separate from the Dashboard server. The Dashboard may write a
small fixed signal to its local SQLite state; it must not accept arbitrary
prompt text as a signal. A suitable record contains a nonce, timestamp, fixed
task name, and state:

```json
{"nonce":"...","at":"...","task":"debug_local_agent","state":"requested"}
```

The monitor claims the nonce before starting work, then updates the state to
`running`, `completed`, or `failed` with a short, redacted result. Do not replay
a claimed nonce after restart. Polling may be frequent because it reads local
state only; GitHub, Gitee, browser, and other network access remain explicit
operations.

## App-server sequence

Run `codex app-server --stdio` under the target repository directory. Keep the
normal permission boundary: `workspace-write`, `on-request`, and network access
disabled unless a separately authorized task needs it.

1. Send `initialize`, then `initialized`.
2. For a known selected ID, send `thread/resume` with the repository `cwd`.
3. If no durable thread exists or resume fails, send `thread/start` with
   `ephemeral: false`, persist its returned `thread.id`, and use that thread.
4. Send `turn/start` with a fixed task prompt. Include the requested model and
   effort only when the user chose them; for example, `gpt-5.6-luna` and
   `medium` are valid explicit settings.
5. Stream status, agent messages, and approval requests into the local UI.
   Mark the signal complete only after `turn/completed` reports completion.

`thread/start` and `turn/start` can create a Codex task visible in the local
Codex desktop/VSCode task list. Visibility is useful evidence, but do not
claim a task ran until `turn/completed` or an equivalent durable output confirms
it.

## Approvals and failure handling

Dashboard routing approval never grants shell or file permissions to Codex.
Forward app-server approval requests to the Dashboard or the client that owns
the app-server session, with allow-once, allow-for-session, and deny choices.
Never convert an approval timeout into acceptance, and never enable bypass
flags for unattended operation.

If app-server cannot initialize its local state, report the sanitized error and
leave the signal failed; do not silently fall back to `codex exec`. If the
selected thread is missing or cannot resume, create a new dedicated thread only
when the user has authorized that fallback, then display and persist its new
ID.

## VSCode companion route

A VSCode companion extension can use the same local state and app-server
sequence. It may display target selection, monitor status, turn output, and
approval requests. This is separate from ChatGPT Web automation; it does not
make a Web conversation resumable through `thread/resume`.
