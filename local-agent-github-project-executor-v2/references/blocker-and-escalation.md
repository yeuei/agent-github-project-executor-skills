# Blocker and Escalation Protocol

## 0. Access failures are different blockers

Keep local and GitHub-side permissions separate:

- **Local Agent Git credential/access** means the local Git client cannot fetch or push because of an SSH key, token, remote URL, network, or local permission. Report the sanitized command/error and the user-owned credential action.
- **ChatGPT GitHub App access** means ChatGPT cannot read, write, create a PR, or update the target repository because the App installation or repository selection is missing. A local Git credential change cannot fix this. In `agent汇报.md`, recommend that the user review the relevant account/organization and repository access at <https://github.com/settings/installations>.

If `coordination.yaml` has `event_protocol: disabled`, or the environment has no Event Hub, that optional integration is not a blocker. Continue local work, reports, commits, and PR collaboration.

## 1. Do not overuse BLOCKED

A task is blocked only when that specific task cannot safely continue.

A blocked task does not imply a blocked PR.

Always identify independent tasks that can proceed.

---

## 2. Level A: engineering issue

Examples:

- missing manifest file;
- missing path;
- schema choice;
- parser bug;
- retry/resume problem;
- logging problem;
- environment issue;
- row-id format;
- deterministic seed;
- output-directory design.

Action:

1. solve it yourself;
2. record the decision;
3. continue;
4. report it in the next current snapshot if relevant.

Do not mark research-level BLOCKED.

---

## 3. Level B: planning/specification issue

Examples:

- unclear dependency;
- two current specs appear inconsistent;
- uncertainty about whether old code is superseded;
- uncertainty about whether a task belongs in the current PR;
- external library behavior needs research.

Action:

1. continue independent tasks;
2. mark only the affected task blocked if truly necessary;
3. write full context to `agent汇报.md`;
4. ask ChatGPT one concrete question.

---

## 4. Level C: research decision

Examples:

- selecting between materially different formal datasets;
- changing final sample count;
- changing model, reward, tool cap, benchmark, admission, teacher, or method.

Action:

1. do not choose silently;
2. mark the affected task waiting-user;
3. report the smallest choice and why it matters;
4. continue all independent work.

---

## 5. Manifest rule

If you say:

> frozen manifest is missing

you must identify what is actually unknown.

You may normally freeze:

- path;
- schema;
- seed;
- row-id;
- hashes;
- deterministic ordering;
- run-id;
- created-at;
- converter hash;
- prompt hash;
- tool registry hash.

Escalate only choices that materially change the formal data or experiment.

---

## 6. Good blocker report

```text
Search-R1 has two 10K candidates:

A: ...
B: ...

Choosing A/B changes formal source provenance, so I did not decide.

All engineering manifest fields are already frozen.

Tool-Star and ReTool are continuing independently.

Need from ChatGPT:
determine whether this is a planning decision or should go to the user.
```

---

## 7. Bad blocker report

```text
Scheme1 BLOCKED because manifest is not frozen.
```

This hides the actual missing decision and unnecessarily stops work.

---

## 8. Waiting rule

Never idle unrelated tasks while waiting for ChatGPT or the user.

The correct pattern is:

```text
blocked task → wait
independent task A → continue
independent task B → continue
```

