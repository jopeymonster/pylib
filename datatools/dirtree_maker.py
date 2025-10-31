#!/usr/bin/env python3
"""
dirtree_maker.py

Provides:
- get_directory_tree(start_path=None, max_depth=None) -> str
- CLI: --start-url / --start-path, --max-path / --max-depth, --output
"""

from __future__ import annotations
import os
import argparse
from typing import Optional, Set


def get_directory_tree(start_path: Optional[str] = None, max_depth: Optional[int] = None) -> str:
    """
    Generate a directory tree string for start_path.

    - If start_path is None, callers are expected to prompt before calling.
    - max_depth: None means unlimited; otherwise positive integer (0 => only header / root line)
    - Returns a string with newline separators (no trailing newline).
    """
    if not start_path:
        raise ValueError("start_path must be provided (pass None only if you will prompt before calling).")

    start_path = os.path.expanduser(start_path)
    if not os.path.exists(start_path):
        return f"Error: The path '{start_path}' does not exist."

    abs_start = os.path.abspath(start_path)
    lines: list[str] = []
    seen_inodes: Set[tuple[int, int]] = set()  # to avoid following symlink loops: (st_dev, st_ino)

    def _safe_scandir(path: str):
        try:
            return list(os.scandir(path))
        except PermissionError:
            return None
        except FileNotFoundError:
            return None

    def _build_tree(path: str, prefix: str = "", depth: int = 0):
        # depth is 0 at root (start_path). If max_depth is set and depth >= max_depth, stop recursing.
        if max_depth is not None and depth >= max_depth:
            return

        entries = _safe_scandir(path)
        if entries is None:
            lines.append(prefix + "└── [Permission Denied or Unreadable]")
            return

        # Sort entries so output is stable: directories first, then files, both alphabetically
        entries_sorted = sorted(entries, key=lambda e: (not e.is_dir(follow_symlinks=False), e.name.lower()))

        for i, entry in enumerate(entries_sorted):
            connector = "└── " if i == len(entries_sorted) - 1 else "├── "
            lines.append(prefix + connector + entry.name)

            # If directory (or symlink to dir), recurse
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError:
                is_dir = False

            if is_dir:
                # avoid symlink loops by checking inode/dev for the target if possible
                try:
                    st = entry.stat(follow_symlinks=False)
                    key = (st.st_dev, st.st_ino)
                    if key in seen_inodes:
                        # loop detected; annotate and skip
                        extension = "    " if i == len(entries_sorted) - 1 else "│   "
                        lines.append(prefix + extension + "└── [symlink/loop detected]")
                        continue
                    seen_inodes.add(key)
                except OSError:
                    # can't stat it, but continue (best effort)
                    pass

                extension = "    " if i == len(entries_sorted) - 1 else "│   "
                _build_tree(entry.path, prefix + extension, depth + 1)

    header = f"Directory tree for: {abs_start}"
    lines.append(header)
    # If start_path is a directory, print its children. If it's a file, just print file as root.
    if os.path.isdir(start_path):
        # print a line for the root itself (optional). Many `tree` outputs show the root folder line.
        # We'll include the root folder name on its own line, then its contents indented.
        root_name = os.path.basename(os.path.normpath(start_path)) or start_path
        lines.append(root_name)
        # start recursion from start_path with depth 0 (children will be depth 0 -> 1)
        _build_tree(start_path, prefix="")
    else:
        # start_path is a file
        lines.append(os.path.basename(start_path))

    return "\n".join(lines)


def _cli():
    parser = argparse.ArgumentParser(description="Generate a directory tree.")
    parser.add_argument(
        "--start-url", "--start-path",
        dest="start_path",
        help="Start directory path (expandable with ~). If omitted, you'll be prompted.",
        default=None,
    )
    parser.add_argument(
        "--max-path", "--max-depth",
        dest="max_depth",
        type=int,
        help="Maximum depth to traverse (0 = only root line). If omitted, traverses fully.",
        default=None,
    )
    parser.add_argument(
        "--output", "-o",
        dest="output",
        help="Write tree to this file instead of printing to stdout.",
        default=None,
    )
    args = parser.parse_args()

    start_path = args.start_path
    if not start_path:
        # interactive prompt
        try:
            prompt = input("Enter directory path (default: current directory): ").strip()
        except (EOFError, KeyboardInterrupt):
            # user cancelled; treat as current directory
            prompt = ""
        start_path = prompt or "."

    # call the function (it will return errors as strings)
    try:
        tree_str = get_directory_tree(start_path=start_path, max_depth=args.max_depth)
    except ValueError as e:
        tree_str = f"Error: {e}"

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(tree_str + "\n")
            print(f"Wrote tree to: {os.path.abspath(args.output)}")
        except OSError as exc:
            print(f"Failed to write to {args.output}: {exc}")
            print(tree_str)
    else:
        print(tree_str)


if __name__ == "__main__":
    _cli()
