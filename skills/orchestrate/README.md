# Orchestrate

Run Codex as a sustained implementation orchestrator for larger plans.

## What It Does

`orchestrate` keeps long implementation work from dissolving into one-off edits. It makes Codex read the plan first, maintain a live status file, turn the plan into ordered todos, delegate bounded parallel work when useful, review worker output before merging, and verify the result before calling the work complete.

Use it when a task has multiple phases, uncertain dependencies, worker coordination, or enough surface area that progress needs a durable status trail.

## When To Use It

Use `orchestrate` for requests like:

- "Use orchestrate to implement this plan."
- "Run this implementation end to end."
- "Resume the plan in `implementation-status.md`."
- "Coordinate workers for the independent parts, then merge the results."

Avoid it for tiny single-file fixes where a normal Codex turn is enough.

## How To Invoke

Mention the skill by name in your request:

```text
Use orchestrate to execute implementation-plan.md end to end.
```

or:

```text
$orchestrate resume the current implementation-status.md and keep going until tests pass.
```

## Expected Workflow

When active, Codex should:

1. Read the plan or status documents first.
2. Create or update `implementation-status.md`.
3. Keep `Current Todo`, `Unearthed Todos`, and `Action Log` current.
4. Spawn workers only for bounded tasks that can run in parallel.
5. Keep critical-path work local while workers run.
6. Review worker output before merging it into the main workspace.
7. Run relevant tests and checks.
8. Re-read the original plan before declaring completion.

The important behavior is completion discipline: finishing the current checklist is not enough if the original plan still has required phases, open exit criteria, or required todos.

## Installation

From this repository:

```bash
cp -R skills/orchestrate ~/.codex/skills/
```

Restart Codex or reload skills after copying.

## Files

- `SKILL.md`: Codex-readable behavior contract.
- `agents/openai.yaml`: agent metadata.
