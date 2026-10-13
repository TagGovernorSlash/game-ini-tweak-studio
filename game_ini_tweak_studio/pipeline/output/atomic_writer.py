"""AtomicWriter — backs up, then writes via temp file + os.replace."""
from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from game_ini_tweak_studio.models.job import Job, JobState
from game_ini_tweak_studio.services.backup_service import BackupService

log = logging.getLogger(__name__)


class AtomicWriter:
    def __init__(self, backups: BackupService, dry_run: bool = False) -> None:
        self._backups = backups
        self._dry_run = dry_run

    def emit(self, job: Job) -> Job:
        if job.patched_text is None:
            job.fail("nothing to emit")
            return job

        if self._dry_run:
            log.info("dry-run: would write %s", job.target)
            job.state = JobState.EMITTED
            return job

        job.backup_path = self._backups.snapshot(job.target)

        target_dir = job.target.parent
        fd, tmp_name = tempfile.mkstemp(prefix=".ini-tweak-", dir=target_dir)
        tmp = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(job.patched_text)
            os.replace(tmp, job.target)
        except OSError as exc:
            tmp.unlink(missing_ok=True)
            job.fail(f"write failed: {exc}")
            return job

        job.state = JobState.EMITTED
        log.info("emitted %s (backup=%s)", job.target, job.backup_path)
        return job