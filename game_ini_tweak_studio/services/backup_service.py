"""BackupService — timestamped snapshots with rotation."""
from __future__ import annotations

import shutil
import time
from pathlib import Path


class BackupService:
    def __init__(self, root: Path, keep: int = 20) -> None:
        self._root = root
        self._keep = keep
        self._root.mkdir(parents=True, exist_ok=True)

    def snapshot(self, target: Path) -> Path:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        dest = self._root / f"{target.name}.{stamp}.bak"
        shutil.copy2(target, dest)
        self._rotate()
        return dest

    def _rotate(self) -> None:
        backups = sorted(self._root.glob("*.bak"), key=lambda p: p.stat().st_mtime)
        for old in backups[: max(0, len(backups) - self._keep)]:
            old.unlink(missing_ok=True)