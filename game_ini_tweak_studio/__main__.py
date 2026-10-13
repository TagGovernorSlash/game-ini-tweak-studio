"""Entry/bootstrap for the game-ini-tweak-studio desktop app."""
from __future__ import annotations

import sys
import logging
from pathlib import Path

from platformdirs import user_log_dir

from game_ini_tweak_studio.app import TweakStudioApp
from game_ini_tweak_studio.config.settings import load_settings


def _configure_logging() -> Path:
    log_dir = Path(user_log_dir("game-ini-tweak-studio", "SamLabs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "studio.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")],
    )
    return log_file


def main(argv: list[str] | None = None) -> int:
    log_file = _configure_logging()
    log = logging.getLogger("studio.bootstrap")
    log.info("game-ini-tweak-studio starting; log=%s", log_file)
    settings = load_settings()
    app = TweakStudioApp(settings)
    return app.run(argv if argv is not None else sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())