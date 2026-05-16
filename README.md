# Eli's Codex Skills

Homemade Codex skills for day-to-day agent workflows.

## Skills

- [Orchestrate](skills/orchestrate/README.md): long-running implementation orchestration.
- [Steer](skills/steer/README.md): mid-task course correction.

Each skill folder contains:

- `README.md`: human instructions, examples, and installation notes.
- `SKILL.md`: Codex-readable skill instructions.
- `agents/openai.yaml`: optional agent metadata.

## Layout

```text
skills/
  orchestrate/
    README.md
    SKILL.md
    agents/openai.yaml
  steer/
    README.md
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
