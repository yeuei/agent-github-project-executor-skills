# Legacy Code and Validation Rules

Before inspecting legacy code, read the actual target repository `README.md` and the current coordination documents. The repository's current task/specification, not the template README or historical runner, defines the work.

## 1. Source of truth

The current implementation requirements come from:

```text
current direct user instruction
>
current 任务.md
>
current chatgpt解惑.md
>
current canonical specification
>
current formal config/manifest
```

Old code is not a specification.

---

## 2. What counts as legacy

Unless explicitly approved as current:

- historical smoke runners;
- superseded branches;
- old prompt runners;
- old tool-call caps;
- old tool schemas;
- old admission logic;
- old evaluation scripts;
- notebooks from previous experiments;
- temporary scripts in old run folders.

---

## 3. What legacy code may be used for

You may:

- read it;
- understand prior implementation patterns;
- reuse general engineering ideas;
- learn from previous bugs and fixes;
- compare behavior against the current requirements.

You should not:

- run it formally just because it once worked;
- copy it unchanged;
- inherit old prompt/cap/schema/admission behavior;
- use its defaults as current project truth.

---

## 4. Approved current components

A component is reusable when current project state explicitly treats it as approved/current.

Examples:

- current canonical parser;
- currently accepted SandboxFusion adapter;
- current prompt source;
- current tool registry;
- current admission implementation.

Even then, verify that the way you call it matches the latest specification.

---

## 5. Correct implementation process

```text
read current task
↓
read current specification
↓
extract required behavior
↓
inspect old code only for experience
↓
implement or adapt to current requirements
↓
run
↓
collect evidence
```

Avoid:

```text
find old runner
↓
change two parameters
↓
formal run
```

unless the current specification explicitly approves that runner.

---

## 6. Validation discipline

Do not create new validation work without a concrete reason.

Allowed reasons:

- the task requires it;
- a real bug needs a minimal reproduction;
- formal-run correctness is at real risk;
- ChatGPT or the user explicitly asks for it.

Do not build chains such as:

```text
smoke
→ smoke of smoke
→ benchmark
→ audit
→ another smoke
```

Validation serves execution.

---

## 7. Smoke vs formal evidence

A smoke run proves only the smoke path.

It does not prove:

- formal data distribution;
- formal run completion;
- final benchmark result;
- final prompt/config correctness for a different run.

Do not mark a formal task done based only on smoke evidence.

For every meaningful run, preserve runtime evidence: command, relevant runtime/tool/dependency versions, input/config identifiers without secrets, run ID or timestamp when useful, exit status, result summary, and log/artifact path. Runtime evidence must support the status reported to ChatGPT; it must not be replaced by file-existence claims.

