"""Top-level app wiring: builds the pipeline and hands it to the GUI."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from game_ini_tweak_studio.config.settings import Settings
from game_ini_tweak_studio.pipeline.registry import build_default_pipeline
from game_ini_tweak_studio.pipeline.runner import PipelineRunner
from game_ini_tweak_studio.services.profile_store import ProfileStore
from game_ini_tweak_studio.services.backup_service import BackupService

log = logging.getLogger(__name__)


@dataclass(slots=True)
class TweakStudioApp:
    settings: Settings

    def run(self, argv: list[str]) -> int:
        store = ProfileStore(self.settings.profiles_dir)
        backups = BackupService(self.settings.backup_dir)
        pipeline = build_default_pipeline(self.settings, store, backups)
        runner = PipelineRunner(pipeline)

        from game_ini_tweak_studio.gui.main_window import MainWindow

        window = MainWindow(runner=runner, store=store, settings=self.settings)
        return window.exec_argv(argv)