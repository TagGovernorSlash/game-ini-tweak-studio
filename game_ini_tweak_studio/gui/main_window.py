"""MainWindow — profile picker, target list, diff view, apply button."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QPlainTextEdit, QLabel, QComboBox,
)
from PySide6.QtCore import Qt

from game_ini_tweak_studio.config.settings import Settings
from game_ini_tweak_studio.models.job import Job
from game_ini_tweak_studio.pipeline.ingest.discovery import DiscoveryIngest
from game_ini_tweak_studio.pipeline.runner import PipelineRunner
from game_ini_tweak_studio.services.profile_store import ProfileStore
from game_ini_tweak_studio.utils.ini_diff import unified_diff


class MainWindow(QMainWindow):
    def __init__(self, runner: PipelineRunner, store: ProfileStore, settings: Settings) -> None:
        super().__init__()
        self.setWindowTitle("game-ini-tweak-studio")
        self.resize(1100, 720)
        self._runner = runner
        self._store = store
        self._settings = settings

        root = QWidget()
        outer = QVBoxLayout(root)

        bar = QHBoxLayout()
        bar.addWidget(QLabel("Profile:"))
        self.profile_box = QComboBox()
        self.profile_box.addItems(store.list_slugs())
        bar.addWidget(self.profile_box, 1)
        self.scan_btn = QPushButton("Scan library")
        bar.addWidget(self.scan_btn)
        self.apply_btn = QPushButton("Apply tweaks")
        bar.addWidget(self.apply_btn)
        outer.addLayout(bar)

        split = QHBoxLayout()
        self.targets = QListWidget()
        self.targets.setSelectionMode(QListWidget.ExtendedSelection)
        split.addWidget(self.targets, 1)
        self.diff = QPlainTextEdit()
        self.diff.setReadOnly(True)
        self.diff.setLineWrapMode(QPlainTextEdit.NoWrap)
        split.addWidget(self.diff, 2)
        outer.addLayout(split, 1)

        self.setCentralWidget(root)
        self.scan_btn.clicked.connect(self._on_scan)
        self.apply_btn.clicked.connect(self._on_apply)
        self._runner.job_done.connect(self._on_job_done)

    def _on_scan(self) -> None:
        slug = self.profile_box.currentText()
        if not slug:
            return
        profile = self._store.load(slug)
        discovery = DiscoveryIngest(self._settings.library_roots)
        self.targets.clear()
        for path in discovery.discover(profile):
            self.targets.addItem(str(path))

    def _on_apply(self) -> None:
        slug = self.profile_box.currentText()
        if not slug:
            return
        profile = self._store.load(slug)
        jobs = [Job(target=__import__("pathlib").Path(self.targets.item(i).text()), profile=profile)
                for i in range(self.targets.count())]
        self._runner.run_async(jobs)

    def _on_job_done(self, job: Job) -> None:
        if job.original_text and job.patched_text:
            self.diff.setPlainText(unified_diff(job.original_text, job.patched_text, job.target.name))

    def exec_argv(self, argv: list[str]) -> int:
        self.show()
        from PySide6.QtWidgets import QApplication
        return QApplication.instance().exec() if QApplication.instance() else 0