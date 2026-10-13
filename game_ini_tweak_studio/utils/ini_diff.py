"""Unified-diff helper for showing before/after in the GUI."""
from __future__ import annotations

import difflib


def unified_diff(before: str, after: str, name: str = "config.ini") -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{name}",
            tofile=f"b/{name}",
        )
    )