# Changelog

## 2026-04-20

- Refactored the Holly internal graph from generic `STRING` payloads to typed Holly contracts.
- Added `core/contracts.py` with `_holly_type` markers and strict payload validation.
- Removed duplicate `target_model` and `user_id` inputs from downstream typed nodes; both now flow from `Holly Input Bundle`.
- Rewired memory nodes so history/profile access consumes `HOLLY_BUNDLE` instead of raw free-form strings.
- Added inspect nodes for every typed Holly payload.
- Added node sanity harness and typed misuse checks.
- Added `NODE_SANITY_MATRIX.md` and `SANITY_BACKLOG.md`.
- Retained `basic_nodes.py` as documented compatibility re-export.
- Preserved existing audit fixes: mixed-case `in` parsing, JSON list handling, user-scoped retrieval, repo hygiene, README, `.gitignore`, tests.

