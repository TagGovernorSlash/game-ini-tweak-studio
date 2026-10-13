"""Wires ingest handlers, processors, and output drivers into a Pipeline."""
from __future__ import annotations

from game_ini_tweak_studio.config.settings import Settings
from game_ini_tweak_studio.pipeline.pipeline import Pipeline
from game_ini_tweak_studio.pipeline.ingest.ini_ingest import IniIngestHandler
from game_ini_tweak_studio.pipeline.ingest.discovery import DiscoveryIngest
from game_ini_tweak_studio.pipeline.processors.ini_patcher import IniPatcher
from game_ini_tweak_studio.pipeline.processors.section_sorter import SectionSorter
from game_ini_tweak_studio.pipeline.output.atomic_writer import AtomicWriter
from game_ini_tweak_studio.services.backup_service import BackupService
from game_ini_tweak_studio.services.profile_store import ProfileStore


def build_default_pipeline(
    settings: Settings, store: ProfileStore, backups: BackupService
) -> Pipeline:
    return Pipeline(
        ingests=[DiscoveryIngest(settings.library_roots), IniIngestHandler()],
        processors=[IniPatcher(), SectionSorter()],
        outputs=[AtomicWriter(backups, settings.dry_run)],
    )