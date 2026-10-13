"""Runtime settings loaded from a JSON file next to the user config dir."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

log = logging.getLogger(__name__)

_APP = "game-ini-tweak-studio"
_AUTHOR = "SamLabs"


@dataclass(slots=True)
class Settings:
    profiles_dir: Path
    backup_dir: Path
    library_roots: list[Path] = field(default_factory=list)
    dry_run: bool = False
    keep_backups: int = 20

    @classmethod
    def defaults(cls) -> "Settings":
        data = Path(user_data_dir(_APP, _AUTHOR))
        return cls(
            profiles_dir=Path(__file__).resolve().parents[2] / "profiles",
            backup_dir=data / "backups",
            library_roots=[
                Path("C:/Program Files (x86)/Steam/steamapps/common"),
                Path("C:/Program Files/Epic Games"),
                Path("C:/GOG Games"),
            ],
        )


def load_settings() -> Settings:
    cfg_path = Path(user_config_dir(_APP, _AUTHOR)) / "settings.json"
    base = Settings.defaults()
    if not cfg_path.exists():
        base.backup_dir.mkdir(parents=True, exist_ok=True)
        return base
    try:
        raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        log.warning("settings.json unreadable (%s); using defaults", exc)
        return base
    base.dry_run = bool(raw.get("dry_run", base.dry_run))
    base.keep_backups = int(raw.get("keep_backups", base.keep_backups))
    if "library_roots" in raw:
        base.library_roots = [Path(p) for p in raw["library_roots"]]
    return base