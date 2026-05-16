---
name: export-clean-repo
description: Export a local development repo into a new clean git-tracked folder with generated artifacts, private planning files, caches, virtualenvs, downloaded model weights, and bulky local outputs excluded. Use when the user asks to make an exportable/public/shareable repo copy, prepare a clean repo from a messy workspace, or rerun the hardcoded export test repo workflow.
---

# Export Clean Repo

Use this skill to produce a fresh, public-oriented repo copy from a local working repo.

## Default Workflow

1. Run the bundled exporter from this skill:

```sh
python /Users/elimaine/code/elis-codex-skills/skills/export-clean-repo/scripts/export_clean_repo.py
```

By default it exports:

- source: `/Users/elimaine/code/delta-mem-mlx`
- destination: `/Users/elimaine/code/delta-mem-mlx-export-clean-test`

2. For a different export, pass explicit paths:

```sh
python /Users/elimaine/code/elis-codex-skills/skills/export-clean-repo/scripts/export_clean_repo.py \
  --source /path/to/source-repo \
  --dest /path/to/new-export-repo
```

3. If the destination already exists and should be replaced, use `--force`. This deletes only the destination path after verifying it is not the source path.

4. Inspect the resulting repo:

```sh
git -C /path/to/new-export-repo status --short
git -C /path/to/new-export-repo log --oneline -1
git -C /path/to/new-export-repo ls-files
```

5. Run project-specific verification in the exported repo before pushing.

## Export Policy

The exporter excludes:

- existing git history and local git metadata;
- virtualenvs, package caches, pytest caches, bytecode, build outputs, node modules;
- local model/checkpoint artifacts such as `.pt`, `.pth`, `.npz`, `.safetensors`, `.gguf`;
- benchmark result folders and scratch/temp folders;
- project build/status/planning notes that should not be in a public export.

It then writes or extends `.gitignore`, runs `git init`, sets branch `main`, stages files, and commits with `Initial clean export`.

## Review Discipline

Treat the export as a draft:

- Scan for private paths, credentials, status files, and large artifacts with `rg` and `find`.
- Confirm docs do not promise local-only integrations.
- Do not push until tests or a justified verification subset pass in the exported repo.
