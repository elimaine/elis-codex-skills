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

Symlink the desired skill directories into your Codex skills directory. This keeps the repo checkout as the source of truth, so edits made here are picked up by Codex without copying files back and forth.

```bash
ln -s "$PWD/skills/orchestrate" ~/.codex/skills/orchestrate
ln -s "$PWD/skills/steer" ~/.codex/skills/steer
```

Restart Codex or reload skills after symlinking.
