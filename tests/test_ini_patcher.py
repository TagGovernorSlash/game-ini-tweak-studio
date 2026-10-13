"""Unit tests for IniPatcher — the core of the pipeline."""
from __future__ import annotations

from pathlib import Path

from game_ini_tweak_studio.models.job import Job
from game_ini_tweak_studio.models.tweak_profile import Tweak, TweakProfile
from game_ini_tweak_studio.pipeline.processors.ini_patcher import IniPatcher


def _profile() -> TweakProfile:
    return TweakProfile(
        slug="t",
        engine="unreal4",
        match=["Engine.ini"],
        tweaks=[
            Tweak(section="SystemSettings", key="r.VSync", value="0"),
            Tweak(section="SystemSettings", key="r.NewKey", value="42"),
        ],
    )


def test_replaces_existing_key(tmp_path: Path) -> None:
    src = tmp_path / "Engine.ini"
    src.write_text("[SystemSettings]\nr.VSync=1\n", encoding="utf-8")
    job = Job