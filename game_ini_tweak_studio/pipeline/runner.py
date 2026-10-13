"""PipelineRunner — GUI-facing façade; runs jobs on a worker thread."""
from __future__ import annotations

from collections.abc import Iterable, Callable

from PySide6.QtCore import QObject, QThread, Signal

from game_ini_tweak_studio.models.job import Job
from game_ini_tweak_studio.pipeline.pipeline import Pipeline


class _JobWorker(QObject):
    finished = Signal(list)
    job_done = Signal(object)

    def __init__(self, pipeline: Pipeline, jobs: list[Job]) -> None:
        super().__init__()
        self._pipeline = pipeline
        self._jobs = jobs

    def run(self) -> None:
        done: list[Job] = []
        for job in self._jobs:
            result = self._pipeline.run_one(job)
            done.append(result)
            self.job_done.emit(result)
        self.finished.emit(done)


class PipelineRunner(QObject):
    job_done = Signal(object)
    all_done = Signal(list)

    def __init__(self, pipeline: Pipeline) -> None:
        super().__init__()
        self._pipeline = pipeline

    def run_async(self, jobs: Iterable[Job]) -> None:
        self._thread = QThread()
        self._worker = _JobWorker(self._pipeline, list(jobs))
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.job_done.connect(self.job_done)
        self._worker.finished.connect(self.all_done)
        self._worker.finished.connect(self._thread.quit)
        self._thread.start()