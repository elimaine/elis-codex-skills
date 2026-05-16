---
name: steer
description: |
  Course-correct an active Codex task without treating the user's message as a new,
  separate request. Use when the user invokes "$steer", says "steer", "course
  correct", "redirect", "actually", "instead", "while you're working", or gives a
  mid-task correction that should reshape the current run. This is the Codex
  version of OpenClaw's /steer behavior: apply the new guidance to the current
  active work, reconcile it with progress so far, and continue from the updated
  instruction.
metadata:
  short-description: Course-correct the active Codex task
---

# Steer

Use this skill when the user is steering an in-progress task. Treat the message
as an update to the current task's intent, constraints, or priority, not as a
fresh standalone request.

## Behavior

1. Identify the steering payload: the text after `$steer`, `steer`, `redirect`,
   `actually`, `instead`, or the user's explicit correction.
2. Fold that payload into the current task immediately.
3. Preserve useful work already done, but stop following any older plan item that
   now conflicts with the steering instruction.
4. If a tool call or command is already complete, use its result; do not rerun it
   unless the new instruction makes it stale.
5. Continue toward the original goal as modified by the steering instruction.

## Response Pattern

If still working, briefly acknowledge the steering and keep moving:

```text
Understood. I am redirecting the current task toward <new constraint> and will adjust the next steps accordingly.
```

Do not produce a final answer just because steering arrived. Finalize only when
the updated task is actually complete or blocked.

## Conflict Handling

- Newer steering beats older instructions at the same priority level.
- System, developer, tool, safety, and explicit permission rules still take
  precedence over the user's steering.
- If the steering asks for a destructive action, external network access, or
  anything requiring approval, request approval through the normal Codex flow.
- If the steering contradicts the original task so much that there is no coherent
  combined goal, ask one concise clarifying question.

## Scope

This skill affects only this Codex thread's current work. It does not control the
Codex UI Steer button, create subagents, steer a different session, or send
messages to an OpenClaw runtime. If the user asks to steer another named agent or
session, use the appropriate available tooling instead.
