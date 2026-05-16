# Eli's Codex Skills

Homemade Codex skills for day-to-day agent workflows.

## Skills

### Orchestrate

`orchestrate` runs a sustained implementation loop for larger tasks. It keeps a live status file, turns plans into ordered todos, coordinates async workers where useful, reviews worker output before merging, and verifies the result before calling work complete.

Use it when you want Codex to execute an implementation plan end to end instead of only making a single isolated change.

### Steer

`steer` course-corrects an active Codex task without treating the correction as a new standalone request. It folds new guidance into the current run, preserves useful work already done, and continues toward the updated goal.

Use it when you need to redirect Codex mid-task with constraints such as "actually use this approach", "instead target this file", or "$steer keep the existing API unchanged".

## Layout

```text
skills/
  orchestrate/
    SKILL.md
    agents/openai.yaml
  steer/
    SKILL.md
    agents/openai.yaml
```

## Install

Copy the desired skill directories into your Codex skills directory:

```bash
cp -R skills/orchestrate ~/.codex/skills/
cp -R skills/steer ~/.codex/skills/
```

Restart Codex or reload skills after copying.
