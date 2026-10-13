"""TweakProfile — a named set of key/value edits for a set of ini files."""
from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class Tweak(BaseModel):
    section: str
    key: str
    value: str
    comment: str | None = None

    @field_validator("value")
    @classmethod
    def _no_newlines(cls, v: str) -> str:
        if "\n" in v or "\r" in v:
            raise ValueError("tweak value must be single-line")
        return v


class TweakProfile(BaseModel):
    slug: str
    engine: str = "custom"
    match: list[str] = Field(min_length=1)
    tweaks: list[Tweak] = Field(min_length=1)
    description: str = ""

    @property
    def file_globs(self) -> list[str]:
        return [m.lower() for m in self.match]

    @classmethod
    def from_path(cls, path: Path) -> "TweakProfile":
        return cls.model_validate_json(path.read_text(encoding="utf-8"))