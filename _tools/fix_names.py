#!/usr/bin/env python3
"""
fix_names.py — enforce snake_case naming across the competencies-db repo.

Processes one top-level folder at a time to support incremental git commits
(HITL workflow). Uses `git mv` to preserve history.

Usage:
    python _tools/fix_names.py [--dry-run]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


# ── Exclusions ────────────────────────────────────────────────────────────────
# Add filenames here to protect them from renaming (exact match, case-sensitive)
EXCLUDED_FILES = [
    "CLAUDE.md",
    "README.md",
    "MEMORY.md",
]

# Top-level directories to skip entirely (not traversed or renamed)
EXCLUDED_DIRS = [
    ".git",
    ".claude",
    "_prompts",
    "_tools",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def find_git_root(start: Path) -> Path:
    current = start.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError(f"No git repository found above {start}")


def to_snake_case(name: str) -> str:
    """Replace hyphens with underscores and lowercase the entire name."""
    return name.replace("-", "_").lower()


def collect_renames(folder: Path) -> list[tuple[Path, Path]]:
    """
    Walk folder bottom-up (deepest first) and collect (old, new) path pairs
    for any name that needs fixing. Does not include the folder root itself —
    the caller appends that last so it is applied after its contents.
    """
    renames: list[tuple[Path, Path]] = []

    for dirpath_str, dirnames, filenames in os.walk(folder, topdown=False):
        dirpath = Path(dirpath_str)

        # Skip subtrees that pass through an excluded directory
        try:
            rel_parts = dirpath.relative_to(folder).parts
        except ValueError:
            continue
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue

        for filename in sorted(filenames):
            if filename in EXCLUDED_FILES:
                continue
            fixed = to_snake_case(filename)
            if fixed != filename:
                renames.append((dirpath / filename, dirpath / fixed))

        for dirname in sorted(dirnames):
            if dirname in EXCLUDED_DIRS:
                continue
            fixed = to_snake_case(dirname)
            if fixed != dirname:
                renames.append((dirpath / dirname, dirpath / fixed))

    return renames


def git_mv(old: Path, new: Path, repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "mv", str(old), str(new)],
        capture_output=True,
        text=True,
        cwd=str(repo_root),
    )
    if result.returncode != 0:
        print(f"    ERROR: {result.stderr.strip()}")
        return False
    return True


# ── Display ───────────────────────────────────────────────────────────────────

def format_rename(old: Path, new: Path, repo_root: Path) -> str:
    try:
        old_rel = old.relative_to(repo_root)
    except ValueError:
        old_rel = old
    return f"  {old_rel}  ->  {new.name}"


# ── Per-folder processing ─────────────────────────────────────────────────────

def process_folder(repo_root: Path, folder: Path, dry_run: bool) -> None:
    renames = collect_renames(folder)

    # Append folder rename last — applied only after its contents are done
    fixed_folder_name = to_snake_case(folder.name)
    folder_rename: tuple[Path, Path] | None = None
    if fixed_folder_name != folder.name:
        folder_rename = (folder, folder.parent / fixed_folder_name)
        renames.append(folder_rename)

    if not renames:
        print(f"  [ok] {folder.name}")
        return

    heading = folder.name
    if folder_rename:
        heading = f"{folder.name}  ->  {fixed_folder_name}"

    bar = "-" * 64
    print(f"\n{bar}")
    print(f"  {heading}")
    print(bar)
    for old, new in renames:
        print(format_rename(old, new, repo_root))

    n = len(renames)
    label = "rename" if n == 1 else "renames"

    if dry_run:
        print(f"\n  {n} {label} - dry run, no changes made.")
        return

    commit_msg = f"Fix ({fixed_folder_name}): snake_case rename folder"
    try:
        input(f"\n  {n} {label} pending. Commit msg: {commit_msg}\n  Press Enter to apply, Ctrl+C to skip this folder... ")
    except KeyboardInterrupt:
        print("\n  Skipped.\n")
        return

    applied = 0
    for old, new in renames:
        if git_mv(old, new, repo_root):
            applied += 1

    status = "OK" if applied == n else "!!"
    print(f"  {status} {applied}/{n} applied.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enforce snake_case naming across the repo, one top-level folder at a time.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Workflow:\n"
            "  1. Run with --dry-run to preview all proposed renames.\n"
            "  2. Run without --dry-run. For each folder with issues, review the\n"
            "     list and press Enter to apply. Then `git commit` before continuing.\n"
            "  3. Ctrl+C skips the current folder without applying anything.\n"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview all proposed renames without making any changes.",
    )
    args = parser.parse_args()

    try:
        repo_root = find_git_root(Path.cwd())
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    top_level = sorted(
        item
        for item in repo_root.iterdir()
        if item.is_dir()
        and item.name not in EXCLUDED_DIRS
        and not item.name.startswith(".")
    )

    if args.dry_run:
        print("DRY RUN - no files will be renamed.\n")

    for folder in top_level:
        process_folder(repo_root, folder, args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
