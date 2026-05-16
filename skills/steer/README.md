# Steer

Course-correct an active Codex task without starting a separate new task.

## What It Does

`steer` tells Codex to treat your latest instruction as a redirect for the current work. Codex should fold the new guidance into the active task, preserve useful progress, stop following now-conflicting plan items, and continue toward the updated goal.

Use it when Codex is already working and you need to change direction, narrow scope, preserve an API, target a different file, or add a constraint.

## When To Use It

Use `steer` for requests like:

- "steer: keep the existing API unchanged."
- "$steer actually target the CLI path first."
- "instead use the existing helper instead of adding a new abstraction."
- "course correct: do not touch the generated files."

Avoid it when you are asking for an unrelated new task. In that case, just make the new request directly.

## How To Invoke

Mention `steer`, `$steer`, or a clear correction while Codex is working:

```text
$steer keep the current UI layout and only change the data loading path.
```

or:

```text
Actually, preserve the old command name and add the new one as an alias.
```

## Expected Workflow

When active, Codex should:

1. Identify the steering payload.
2. Apply it to the current task immediately.
3. Keep completed work that still fits.
4. Stop following older plan items that now conflict.
5. Continue working instead of producing a premature final answer.

If the correction makes the task incoherent, Codex should ask one concise clarifying question.

## Installation

From this repository:

```bash
cp -R skills/steer ~/.codex/skills/
```

Restart Codex or reload skills after copying.

## Files

- `SKILL.md`: Codex-readable behavior contract.
- `agents/openai.yaml`: agent metadata.
