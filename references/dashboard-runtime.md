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

`start` is idempotent and waits for the localhost endpoint. `status` probes
`/api/status`, reports reachability and recorded process identity, and must be
checked against the returned repository path. Restart means `stop`, `start`,
then `status`.

If the port is occupied, inspect the status payload and use an explicit
alternate `--port`; never kill an unknown process. On failure preserve the
`/tmp` log path and exact error. `stop` only terminates the PID recorded by the
launcher.

## Runtime/API boundary

The Dashboard observes the handoff project's event history, historical task
snapshots, and binding.v1 state through `/api/status`, event/task-history
endpoints, and `/api/bindings`. The handoff project remains the source of truth;
the skill only schedules and observes the runtime. Tokens, full conversation
URLs, and private payloads must not appear in output, logs, or reports.
