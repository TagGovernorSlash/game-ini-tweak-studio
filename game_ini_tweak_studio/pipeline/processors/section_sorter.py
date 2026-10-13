"""SectionSorter — optional processor that keeps section order stable."""
from __future__ import annotations

from game_ini_tweak_studio.models.job import Job, JobState


class SectionSorter:
    """No-op by default; subclass or toggle via settings to enforce ordering."""

    def __init__(self, enabled: bool = False) -> None:
        self._enabled = enabled

    def process(self, job: Job) -> Job:
        if not self._enabled or job.patched_text is None:
            return job
        # Stable sort of section blocks while preserving comments attached above.
        blocks: list[tuple[str, list[str]]] = []
        header: list[str] = []
        current: list[str] = header
        current_name = ""
        for line in job.patched_text.splitlines():
            if line.lstrip().startswith("[") and line.rstrip().endswith("]"):
                current_name = line.strip()
                current = []
                blocks.append((current_name, current))
            current.append(line)
        ordered = header + [ln for _, block in sorted(blocks) for ln in block]
        job.patched_text = "\n".join(ordered) + "\n"
        job.state = JobState.PROCESSED
        return job