# Security Policy

## Supported versions

| Version   | Supported |
|-----------|-----------|
| 2026.x    | yes       |
| 2025.x    | no        |

## Scope

game-ini-tweak-studio reads and writes user-owned config files inside game
install directories. It does not phone home, does not bundle telemetry, and
does not require network access at runtime.

## What we consider a vulnerability

- Path traversal in the ingest handler that lets a profile write outside the
  declared game root.
- Backup bypass: any code path that mutates an `.ini` without first writing a
  timestamped backup to `backups/`.
- Unsafe profile loading: a `profiles/*.json` that executes code (it never
  should — profiles are pure data).
- Privilege escalation via the Windows service helper (not yet shipped).

## Reporting

Email `security@game-ini-tweak-studio.dev` with a repro. Do not open a public
issue for path-traversal or backup-bypass bugs. We aim to acknowledge within
72 hours.

## Out of scope

- Game anti-cheat bans resulting from tweaked configs. Tweak at your own risk;
  some titles flag modified `.ini` files.
- Third-party profiles you downloaded from a forum.