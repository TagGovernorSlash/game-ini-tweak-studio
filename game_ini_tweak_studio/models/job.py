"""Job — one unit of work flowing through the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from game_ini_tweak_studio.models.tweak_profile import TweakProfile


class JobState(str, Enum):
    PENDING = "pending"
    INGESTED = "ingested"
    PROCESSED = "processed"
    EMITTED = "emitted"
    FAILED = "failed"


@dataclass(slots=True)
class Job:
    target: Path
    profile: TweakProfile
    state: JobState = JobState.PENDING
    original_text: str | None = None
    patched_text: str | None = None
    backup_path: Path | None = None
    errors: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.errors.append(msg)
        self.state = JobState.FAILED