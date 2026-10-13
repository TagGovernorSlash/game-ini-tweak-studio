"""IniIngestHandler — reads raw text + detects line ending + BOM."""
from __future__ import annotations

import logging
from game_ini_tweak_studio.models.job import Job, JobState

log = logging.getLogger(__name__)


class IniIngestHandler:
    def handle(self, job: Job) -> Job:
        try:
            raw = job.target.read_bytes()
        except OSError as exc:
            job.fail(f"read failed: {exc}")
            return job

        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig" if bom else "utf-8", errors="replace")
        # Preserve CRLF vs LF for round-trip fidelity.
        job.original_text = text
        job.state = JobState.INGESTED
        log.debug("ingested %s (bom=%s, %d bytes)", job.target, bom, len(raw))
        return job