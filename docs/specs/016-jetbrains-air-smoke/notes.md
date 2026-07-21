# 016 — jetbrains-air-smoke — notes

_Created 2026-07-21._

## Preflight

- Neither `jetbrains-toolbox` nor `air` is present on `PATH`.
- No Air application was found under the standard JetBrains Toolbox app directories or `/opt`.
- Display variables exist, but no installed application is available to launch.
- JetBrains Toolbox App 3.6.2 is current in the official release API on 2026-07-21.
- Official JetBrains Linux installation documentation requires the Toolbox UI and states that silent Linux installation is not available.

## Decision

Deferred rather than fabricating a smoke result or promoting readiness from marketing evidence. Resume with the interactive installation/authentication session, then use the exact commands in `plan.md`.
