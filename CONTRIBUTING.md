# Contributing to game-ini-tweak-studio

Thanks for wanting to help tune game configs. This repo is a Windows desktop
GUI that ingests `.ini` / `.cfg` / `.conf` files from game installs, applies
tweak profiles, and writes them back with backups. It is a pipeline: ingest →
process → emit.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m game_ini_tweak_studio
```

## Branching

- `main` is stable, tagged per release (e.g. `v2026.02`).
- Feature work goes on `feat/<short-name>`.
- Tweak-profile additions go on `profile/<game-slug>`.

## Tweak profiles

Profiles live in `profiles/`. Each is a JSON file with:

```json
{
  "slug": "ue4-shooter-lowlatency",
  "engine": "unreal4",
  "match": ["Engine.ini", "GameUserSettings.ini"],
  "tweaks": [
    {"key": "r.OneFrameThreadLag", "value": "0", "section": "SystemSettings"},
    {"key": "bUseVSync", "value": "False", "section": "/Script/Engine.GameUserSettings"}
  ]
}
```

Every profile MUST declare `match` globs (never a hardcoded absolute path) so
the ingest handler can locate files across Steam / Epic / GOG installs.

## Code style

- `ruff` + `black` (line length 100).
- Type hints everywhere. `mypy --strict` on `core/` and `pipeline/`.
- No bare `except:`. Use `except (OSError, ValueError) as exc:` and log.
- GUI code (PySide6) stays in `gui/` and never touches the filesystem directly —
  it dispatches through `pipeline/`.

## Tests

```powershell
pytest -q
```

Add a fixture under `tests/fixtures/` for any new INI dialect you support.

## Reporting bugs

Open an issue with: game name, engine, ini path, before/after diff, and the
profile slug you used. Attach the `*.log` from `%LOCALAPPDATA%\game-ini-tweak-studio\`.