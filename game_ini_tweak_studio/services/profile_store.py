"""ProfileStore — loads and validates TweakProfile JSON files."""
from __future__ import annotations

import logging
from pathlib import Path

from game_ini_tweak_studio.models.tweak_profile import TweakProfile

log = logging.getLogger(__name__)


class ProfileStore:
    def __init__(self, root: Path) -> None:
        self._root = root

    def list_slugs(self) -> list[str]:
        if not self._root.exists():
            return []
        return sorted(p.stem for p in self._root.glob("*.json"))

    def load(self, slug: str) -> TweakProfile:
        path = self._root / f"{slug}.json"
        return TweakProfile.from_path(path)

    def load_all(self) -> list[TweakProfile]:
        out: list[TweakProfile] = []
        for slug in self.list_slugs():
            try:
                out.append(self.load(slug))
            except Exception as exc:  # noqa: BLE001 — one bad profile shouldn't kill the list
                log.warning("profile %s invalid: %s", slug, exc)
        return out