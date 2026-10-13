"""Pipeline — chains ingest → process → emit over a list of Jobs."""
from __future__ import annotations

import logging
from collections.abc import Iterable, Sequence
from typing import Protocol

from game_ini_tweak_studio.models.job import Job, JobState

log = logging.getLogger(__name__)


class IngestHandler(Protocol):
    def handle(self, job: Job) -> Job: ...


class Processor(Protocol):
    def process(self, job: Job) -> Job: ...


class OutputDriver(Protocol):
    def emit(self, job: Job) -> Job: ...


class Pipeline:
    def __init__(
        self,
        ingests: Sequence[IngestHandler],
        processors: Sequence[Processor],
        outputs: Sequence[OutputDriver],
    ) -> None:
        self._ingests = list(ingests)
        self._processors = list(processors)
        self._outputs = list(outputs)

    def run_one(self, job: Job) -> Job:
        for stage in (*self._ingests, *self._processors, *self._outputs):
            if job.state is JobState.FAILED:
                break
            try:
                job = stage.handle(job) if stage in self._ingests else (
                    stage.process(job) if stage in self._processors else stage.emit(job)
                )
            except Exception as exc:  # noqa: BLE001 — job-level isolation
                log.exception("stage %s failed on %s", type(stage).__name__, job.target)
                job.fail(f"{type(stage).__name__}: {exc}")
        return job

    def run(self, jobs: Iterable[Job]) -> list[Job]:
        return [self.run_one(j) for j in jobs]