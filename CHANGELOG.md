# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - unreleased

### Added

- `proof-before-done` plugin: a PostToolUse read-back reminder and a Stop check that asks once for proof before a "done" claim about an external write, `scripts/backtest.py`, and the `self-correct` skill.
- `operating-rules` plugin: an opt-in SessionStart hook that injects a compact version of the eight operating rules.
- `session-handoff` plugin: the `session-handoff` skill (one lean STATUS.md, read back before the receipt).
- `knowledge-compounding` plugin: the `knowledge-base` skill.
- `product-workflows` plugin: the `market-research`, `prd` and `decision-ledger` skills.
- `pm-routines` plugin: the `market-sweep`, `weekly-metrics-review` and `watch-until` routines, plus `SCHEDULING.md`.
- `templates/CLAUDE.md` (the eight operating rules and the settings keys) and `templates/settings.example.json`.
- Privacy lint, skill checker, markdown link checker, and CI (strict validation, unit tests, lint, link check, gitleaks).
- Eval case `self-correct-three-copies`.
- README, lab notebook with entries 001 to 004, `docs/how-i-work.md`, contributing guide and issue templates.
