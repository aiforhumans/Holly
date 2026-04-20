# Holly Prompt

Holly Prompt is a ComfyUI custom node package for prompt orchestration, typed internal graph flow, and local prompt-memory utilities.

The package is split by responsibility:
- `nodes/`: ComfyUI-facing node classes
- `core/`: payload contracts and prompt logic
- `services/`: SQLite-backed history and profile storage
- `tests/`: unit tests and node sanity harness

## Installation

Place the package at:

```text
F:\ComfyUI_windows_portable\ComfyUI\custom_nodes\Holly_prompt
```

Restart ComfyUI. Holly nodes appear under:
- `Holly/Prompting`
- `Holly/Core`
- `Holly/Memory`
- `Holly/Inspect`

## Node Categories

### Holly/Prompting
- `Prompt Prefix`
- `Prompt + Image Tags`

These are edge utility nodes. They stay `STRING`-based and are intended to feed `Holly Input Bundle`.

### Holly/Core
- `Holly Input Bundle`
- `Holly Intent Analyze`
- `Holly Semantic Expand`
- `Holly Integrity Validate`
- `Holly Strategy Select`
- `Holly Blueprint Build`
- `Holly Model Formatter`
- `Holly Prompt Compare`

These nodes use typed Holly payloads internally:
- `HOLLY_BUNDLE`
- `HOLLY_INTENT`
- `HOLLY_SEMANTIC_CANDIDATES`
- `HOLLY_VALIDATED_SEMANTICS`
- `HOLLY_STRATEGY`
- `HOLLY_BLUEPRINT`

### Holly/Memory
- `Holly Trace Save`
- `Holly History Retrieve`
- `Holly Preference Profile`
- `Holly History Filter`
- `Holly Session Viewer`

These nodes use:
- `HOLLY_HISTORY_HITS`
- `HOLLY_PROFILE`
- `HOLLY_REUSABLE_PATTERNS`

### Holly/Inspect
- `Holly Bundle Inspect`
- `Holly Intent Inspect`
- `Holly Semantics Inspect`
- `Holly Strategy Inspect`
- `Holly Blueprint Inspect`
- `Holly History Hits Inspect`
- `Holly Profile Inspect`
- `Holly Reusable Patterns Inspect`

These are explicit adapter/debug nodes that expose typed payloads as readable `STRING` output.

## Recommended Graph Flow

### Core flow
1. `Prompt Prefix` or `Prompt + Image Tags` (optional edge utility)
2. `Holly Input Bundle`
3. `Holly Intent Analyze`
4. `Holly Semantic Expand`
5. `Holly Integrity Validate`
6. `Holly Strategy Select`
7. `Holly Blueprint Build`
8. `Holly Model Formatter`
9. `Holly Prompt Compare`

### Memory loop
1. `Holly Input Bundle`
2. `Holly History Retrieve`
3. `Holly History Filter`
4. `Holly Semantic Expand` and/or `Holly Strategy Select`
5. `Holly Trace Save`
6. `Holly Session Viewer`

### Inspect/debug flow
Connect any typed Holly payload into the matching inspect node to see its JSON representation.

## Storage

Trace history is stored in:

```text
Holly_prompt/data/holly_prompt.db
```

Use `HOLLY_PROMPT_DB_PATH` to override the database path in tests or external tooling.

## Development

Run tests:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Compatibility note:
- `basic_nodes.py` is intentionally retained as a backward-compatible re-export of the prompt utility nodes.

## Known Limits

- `Prompt + Image Tags` requires an `IMAGE` connection but does not inspect the image tensor itself.
- Intent analysis and strategy selection are heuristic, not LLM-driven.
- History retrieval uses token overlap, not embeddings or semantic search.
- `mode` and `target_model` are still free-form widget strings at the bundle edge.

