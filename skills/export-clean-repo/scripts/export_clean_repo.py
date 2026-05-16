#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import subprocess
from pathlib import Path


DEFAULT_SOURCE_REPO = Path("/Users/elimaine/code/delta-mem-mlx")
DEFAULT_DEST_REPO = Path("/Users/elimaine/code/delta-mem-mlx-export-clean-test")

DROP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "dist",
    "build",
    "coverage",
    "htmlcov",
    "models",
    "adapters",
    "state",
    "tmp",
    "scratch",
}

DROP_REL_DIRS = {
    "benchmarks/results",
}

DROP_FILE_NAMES = {
    ".DS_Store",
    "DETACH_CHEATSHEET.md",
}

DROP_FILE_PATTERNS = {
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    "*.dylib",
    "*.egg-info",
    "*.tsbuildinfo",
    "*.bench.json",
    "*.safetensors",
    "*.gguf",
    "*.pt",
    "*.pth",
    "*.npz",
    ".env",
    ".env.*",
    "package-lock.json",
    "implementation-plan*",
    "implementation-status*",
    "project-build-status*",
    "build-status*",
}

GITIGNORE_BLOCK = """# Python
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Environments
.venv/
venv/
env/
.env
.env.*

# Node / build output
node_modules/
dist/
build/
coverage/
*.tsbuildinfo

# Local model/cache artifacts
models/
adapters/
state/
*.safetensors
*.gguf
*.pt
*.pth
*.npz

# Benchmark outputs
benchmarks/results/
*.bench.json

# Local editor/system files
.DS_Store
.idea/
.vscode/

# Project-local scratch
tmp/
scratch/
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a clean git-tracked copy of a local repo.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE_REPO)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST_REPO)
    parser.add_argument("--force", action="store_true", help="Replace destination if it already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without copying or committing.")
    parser.add_argument("--commit-message", default="Initial clean export")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    dest = args.dest.expanduser().resolve()
    validate_paths(source, dest, force=args.force)

    if args.dry_run:
        print(json.dumps({"source": str(source), "dest": str(dest), "force": args.force}, indent=2))
        return 0

    if dest.exists():
        shutil.rmtree(dest)
    copy_clean(source, dest)
    ensure_gitignore(dest)
    init_git(dest, args.commit_message)
    summary = {
        "source": str(source),
        "dest": str(dest),
        "tracked_files": int(run(["git", "ls-files"], cwd=dest, capture=True).count("\n")),
        "commit": run(["git", "rev-parse", "--short", "HEAD"], cwd=dest, capture=True).strip(),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def validate_paths(source: Path, dest: Path, *, force: bool) -> None:
    if not source.exists():
        raise SystemExit(f"source repo does not exist: {source}")
    if not source.is_dir():
        raise SystemExit(f"source is not a directory: {source}")
    if source == dest:
        raise SystemExit("destination must differ from source")
    if source in dest.parents:
        raise SystemExit("destination must not be inside the source repo")
    if dest.exists() and not force:
        raise SystemExit(f"destination exists; pass --force to replace it: {dest}")


def copy_clean(source: Path, dest: Path) -> None:
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if should_drop(path, rel):
            continue
        target = dest / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        elif path.is_symlink():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(path.readlink())
    remove_private_path_files(dest, source)


def should_drop(path: Path, rel: Path) -> bool:
    rel_posix = rel.as_posix()
    parts = set(rel.parts)
    if parts & DROP_DIR_NAMES:
        return True
    if any(fnmatch.fnmatch(part, "*.egg-info") for part in rel.parts):
        return True
    if any(rel_posix == item or rel_posix.startswith(f"{item}/") for item in DROP_REL_DIRS):
        return True
    if path.name in DROP_FILE_NAMES:
        return True
    return any(fnmatch.fnmatch(path.name, pattern) for pattern in DROP_FILE_PATTERNS)


def remove_private_path_files(dest: Path, source: Path) -> None:
    private_markers = {
        str(Path.home()),
        str(source),
    }
    for path in sorted(dest.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(marker and marker in text for marker in private_markers):
            path.unlink()


def ensure_gitignore(dest: Path) -> None:
    path = dest / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = "# export-clean-repo defaults"
    block = f"\n{marker}\n{GITIGNORE_BLOCK}"
    if marker not in existing:
        text = existing.rstrip() + block if existing.strip() else f"{marker}\n{GITIGNORE_BLOCK}"
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def init_git(dest: Path, commit_message: str) -> None:
    run(["git", "init"], cwd=dest)
    run(["git", "branch", "-M", "main"], cwd=dest)
    run(["git", "add", "."], cwd=dest)
    run(["git", "commit", "-m", commit_message], cwd=dest)


def run(args: list[str], *, cwd: Path, capture: bool = False) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        check=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    return result.stdout if capture else ""


if __name__ == "__main__":
    raise SystemExit(main())
