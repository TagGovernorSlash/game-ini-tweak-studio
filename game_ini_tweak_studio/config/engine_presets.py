"""Known engine fingerprints used to guess which dialect an INI file is."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnginePreset:
    name: str
    comment_prefixes: tuple[str, ...]
    section_brackets: tuple[str, str]
    key_value_sep: tuple[str, ...]


PRESETS: dict[str, EnginePreset] = {
    "unreal4": EnginePreset("unreal4", (";", "#"), ("[", "]"), ("=",)),
    "unity": EnginePreset("unity", (";", "#"), ("[", "]"), ("=", ":")),
    "source": EnginePreset("source", ("//",), ("\"", "\""), (" ", "\t")),
    "idtech": EnginePreset("idtech", ("//",), ("{", "}"), (" ", "\t")),
    "custom": EnginePreset("custom", (";", "#", "//"), ("[", "]"), ("=", ":")),
}


def guess_engine(sample: str) -> EnginePreset:
    """Cheap heuristic: sniff comment style + section brackets from a sample."""
    for name, preset in PRESETS.items():
        if name == "custom":
            continue
        if any(line.lstrip().startswith(p) for p in preset.comment_prefixes for line in sample.splitlines()):
            return preset
    return PRESETS["custom"]