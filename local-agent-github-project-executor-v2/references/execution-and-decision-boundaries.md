# Execution and Decision Boundaries

## 0. Repository entry boundary

The protocol template is not a project workspace. Do not execute real project work in `template_chatgpt_github_codex`. An initialized or mature target handoff must be read and resumed in place; do not reinitialize it or fabricate a PR directory.

## 1. Agent-autonomous decisions

Unless the current specification says otherwise, the Agent should decide:

- manifest file path;
- manifest schema;
- deterministic seed implementation;
- stable row-id representation;
- JSON vs JSONL;
- atomic writes;
- retry/backoff implementation;
- logging format;
- resume implementation;
- checkpoint naming;
- run folder naming;
- module decomposition;
- worker/process organization;
- queue/batch engineering;
- hash computation;
- lineage serialization;
- ordinary parser fixes;
- local dependency/environment fixes;
- ordinary performance fixes that preserve semantics.

These are engineering reproducibility choices, not research decisions.

Record them and continue.

---

## 2. ChatGPT-level decisions

Escalate to ChatGPT when the issue is about:

- task ordering;
- whether two tasks can run in parallel;
- whether a blocker truly blocks the mainline;
- how to interpret current project rules;
- whether a historical implementation is superseded;
- whether an implementation satisfies the current specification;
- whether external research is needed;
- whether a newly discovered task belongs in the current PR.

---

## 3. User-level decisions

Do not decide these autonomously when they materially change the experiment:

- formal dataset choice among materially different sources;
- final data sample count;
- final mixture proportions;
- model replacement;
- reward-method change;
- reward weighting that changes the method;
- tool-call cap;
- admission-rule change;
- benchmark or split;
- teacher-model change;
- formal prompt objective change;
- algorithmic route;
- paper-level research claim.

When such a decision is needed:

- mark the affected task waiting-user through the coordination process;
- continue unrelated work;
- report the smallest unresolved choice.

---

## 4. Engineering vs research test

Ask:

> If I choose differently, could this materially change the experimental conclusion, method definition, or formal comparison?

If no:

> likely engineering; decide and document.

If yes:

> escalate.

---

## 5. User instructions override

A current explicit user instruction has the highest normative priority.

Do not use an older document or runner to override it.

If the user instruction has not yet been written into GitHub and you received it directly, execute it and ensure the repository coordination state is updated accordingly.

## 6. Three-party permission boundary

- The **user** owns project intent, sensitive authorization, material research decisions, and final decisions.
- **ChatGPT** coordinates GitHub-side state and communication when its GitHub App can access the target repository.
- The **Agent** owns local inspection, implementation, experiments, validation, evidence, reports, and ordinary Git operations permitted by its local environment.

Do not claim another party's access. A local Git credential issue and a ChatGPT GitHub App installation issue must be reported and resolved through their respective owners.

