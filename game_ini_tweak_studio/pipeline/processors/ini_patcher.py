"""IniPatcher — applies profile tweaks to text while preserving structure."""
from __future__ import annotations

import re
from game_ini_tweak_studio.models.job import Job, JobState

_SECTION_RE = re.compile(r"^\s*\[(?P<name>[^\]]+)\]\s*$")
_KV_RE = re.compile(r"^(?P<lead>\s*)(?P<key>[^=:#]+?)(?P<sep>\s*[=:]\s*)(?P<val>.*?)(?P<tail>\s*)$")


class IniPatcher:
    def process(self, job: Job) -> Job:
        if job.original_text is None:
            job.fail("no ingested text")
            return job

        wanted: dict[tuple[str, str], str] = {
            (t.section, t.key): t.value for t in job.profile.tweaks
        }
        seen: set[tuple[str, str]] = set()
        out_lines: list[str] = []
        current_section = ""

        for line in job.original_text.splitlines():
            m = _SECTION_RE.match(line)
            if m:
                current_section = m.group("name").strip()
                out_lines.append(line)
                continue

            kv = _KV_RE.match(line)
            if kv and not line.lstrip().startswith((";", "#", "//")):
                key = kv.group("key").strip()
                token = (current_section, key)
                if token in wanted:
                    seen.add(token)
                    out_lines.append(
                        f"{kv.group('lead')}{kv.group('key')}{kv.group('sep')}{wanted[token]}"
                    )
                    continue

            out_lines.append(line)

        # Append tweaks whose section/key didn't exist yet.
        missing = [t for t in job.profile.tweaks if (t.section, t.key) not in seen]
        if missing:
            out_lines.append("")
            by_section: dict[str, list] = {}
            for t in missing:
                by_section.setdefault(t.section, []).append(t)
            for section, tweaks in by_section.items():
                out_lines.append(f"[{section}]")
                for t in tweaks:
                    out_lines.append(f"{t.key}={t.value}")

        job.patched_text = "\n".join(out_lines) + "\n"
        job.state = JobState.PROCESSED
        return job