"""DiscoveryIngest — finds candidate ini files under configured library roots."""
from __future__ import annotations

import logging
from pathlib import Path

from game_ini_tweak_studio.models.job import Job, JobState

log = logging.getLogger(__name__)

_SKIP_DIRS = {"$recycle.bin", "system volume information", "windows"}


class DiscoveryIngest:
    def __init__(self, roots: list[Path], max_depth: int = 4) -> None:
        self._roots = [r for r in roots if r.exists()]
        self._max_depth = max_depth

    def discover(self, profile) -> list[Path]:
        wanted = set(profile.file_globs)
        found: list[Path] = []
        for root in self._roots:
            for path in self._walk(root):
                if path.name.lower() in wanted:
                    found.append(path)
        return found

    def _walk(self, root: Path):
        stack: list[tuple[Path, int]] = [(root, 0)]
        while stack:
            cur, depth = stack.pop()
            if depth > self._max_depth:
                continue
            try:
                for child in cur.iterdir():
                    if child.is_dir():
                        if child.name.lower() in _SKIP_DIRS:
                            continue
                        stack.append((child, depth + 1))
                    else:
                        yield child
            except (OSError, PermissionError) as exc:
                log.debug("skip %s: %s", cur, exc)

    def handle(self, job: Job) -> Job:
        if job.target.exists():
            job.state = JobState.INGESTED
        else:
            job.fail(f"target missing: {job.target}")
        return job