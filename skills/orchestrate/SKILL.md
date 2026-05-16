---
name: orchestrate
description: Long-running implementation orchestration loop for executing plans end to end. Use when the user asks Codex to read or create implementation plans/status files, maintain a running todo/action log, coordinate async workers/subagents, split dependent work, merge reviewed worker output, clean up temp folders, and keep going until implementation and tests are complete.
---

# Orchestrate

Use this skill to run a sustained implementation loop as an orchestrator: keep the main repo coherent, delegate isolated work to workers, merge only reviewed results, and keep status files accurate.

## Core Loop

1. Read existing planning/status docs first:
   - Prefer explicit files named by the user.
   - Otherwise look for `implementation-plan.md`, `implementation-plan-*`, `PLAN.md`, `TODO.md`, `implementation-status.md`, or nearby equivalents.
2. Create or update a status file:
   - Prefer an existing `implementation-status.md`.
   - If absent, create `implementation-status.md`.
   - Include `Operating Model`, `Current Todo`, `Unearthed Todos`, and `Action Log`.
3. Turn the plan into an ordered todo list:
   - Put dependency blockers first.
   - Mark independent tracks that can run in parallel.
   - Keep one list as the source of truth; do not let side notes drift.
4. Spawn async workers only for bounded, parallelizable tasks:
   - Give each worker only the context it needs.
   - Assign a unique temp folder and, for code edits, a clear write scope.
   - Tell workers they are not alone in the codebase.
   - Tell workers not to edit the main repo and not to revert others' work.
5. Continue local critical-path work while workers run.
6. Review worker output before merge:
   - Read changed files directly.
   - Run relevant tests in the worker folder if possible.
   - Copy or reimplement only the parts that hold up.
   - Fix obvious integration issues during merge.
7. Verify in the main repo:
   - Run tests/checks that prove the completed todos.
   - If dependencies are missing, install or otherwise resolve them instead of stopping with the todo incomplete, unless installation is impossible or unsafe.
   - Record any remaining verification gaps explicitly.
8. Clean up accepted worker temp folders after merge.
9. Update `implementation-status.md` after every meaningful step:
   - Mark completed todos.
   - Add newly discovered todos.
   - Record worker starts/completions, merge decisions, test outcomes, and cleanup.
10. Keep going until the current todo list is complete or a real blocker remains.

## Resume Existing Work

When resuming an interrupted or previous orchestration:

1. Read `implementation-status.md` before making changes.
2. Reconstruct state from the status file:
   - Current todo list and first unchecked item.
   - `[~]` in-progress items.
   - Recent `Action Log` entries.
   - Open verification gaps.
   - Worker temp folders or async sessions mentioned in the log.
3. Check whether referenced workers or temp folders still exist:
   - If a worker is still running, ask it for status or wait only when its result blocks the next step.
   - If a worker was interrupted, inspect its temp folder before discarding it.
   - If temp output is useful, review and merge it through normal merge discipline.
4. Continue from the earliest dependency-blocking incomplete todo.
5. Do not redo completed work unless verification shows it is invalid.
6. Update `implementation-status.md` immediately with the resume decision:
   - What state was found.
   - Which todo is active.
   - Which worker/temp artifacts are being reused or discarded.

## Status File Shape

Use this minimal structure:

```markdown
# Implementation Status

## Operating Model

- Main workspace: `<absolute path>`
- Plan source: `<file or user request>`
- Worker policy: workers use isolated temp folders, test there, report back, then orchestrator reviews and merges selected work.
- Cleanup policy: accepted worker temp folders are removed after merge.

## Current Todo

1. [x] Completed item.
2. [~] In-progress item.
3. [ ] Pending item.

## Unearthed Todos

- [ ] New todo discovered while implementing.

## Action Log

- Completed todo 1: concise factual note.
- Started Worker A in `/private/tmp/...` for `<scope>`.
- Verification: `<command>` passed/failed with reason.
```

Use `[~]` for in progress. Keep todos ordered by execution dependency, not discovery order. Move or rewrite todos as the work becomes clearer.

## Worker Prompts

Use yolo-style worker instructions where the harness allows it, but stay inside tool and sandbox rules.

Template:

```text
Context: main workspace is <path>. It contains <plan/status files>.
You are Worker <name>. You are not alone in the codebase; do not edit the main workspace and do not revert edits made by others.
Work only in <temp folder>.
Do not request approval or wait on permission-gated/network/dependency actions. If blocked, use available tools inside the temp folder or report the blocker.
Task: <bounded task>.
If coding, test in your temp folder.
Final response must include changed files, commands attempted, test results, assumptions, and temp artifacts created.
```

Good worker tasks:

- "Research upstream repo layout and APIs; report exact files/functions."
- "Draft a scaffold in `/private/tmp/project-sidecar`; include tests with fake dependencies."
- "Implement one module with a disjoint write scope."
- "Run an independent verification pass against already merged work."

Poor worker tasks:

- Vague "work on the project."
- Immediate blocking work the orchestrator needs before doing anything else.
- Tasks that require editing the same files as another worker.
- Tasks that require hidden user context not included in the prompt.

## Merge Discipline

Treat worker output as a draft, not truth.

- Inspect files before copying.
- Prefer `apply_patch` for hand-merged changes in the main repo.
- Preserve user changes and unrelated edits.
- Do not blindly copy generated caches, virtualenvs, lockfiles, or local artifacts.
- When a worker could not test because dependencies were missing, either install/run the tests yourself or keep the verification todo open.
- Remove temp folders only after accepted work is merged and status is updated.

## Verification Discipline

Do not mark implementation todos complete just because files exist.

- For Python: run unit tests; if missing packages block tests, install into a local venv or use the repo's dependency tool when appropriate.
- For frontend: run build/lint/tests and browser QA when relevant.
- For docs-only changes: run link/syntax checks when available and at least inspect rendered/structured output if applicable.
- For generated CLIs/scripts: run `--help` and at least one representative dry run.

If verification genuinely cannot be completed, leave a specific open todo such as:

```markdown
12. [ ] Run sidecar tests in an environment with FastAPI/pytest installed.
```

## Lessons Learned

- Keep a live `implementation-status.md`; it prevents long-running orchestration from losing state.
- Worker temp folders let workers move fast without risking main repo churn.
- Workers may hang on permission prompts; give explicit no-approval/yolo instructions and interrupt stale workers for status.
- A worker can produce useful files even if it never returns; inspect the temp folder before abandoning it.
- Missing test dependencies are not a stopping point by themselves. Install or create the needed environment when reasonable, then run the tests.
- Record exact verification failures. Future agents need to know whether a failure was code, environment, dependency, or sandbox.
- Close workers once their output has been reviewed and merged.
