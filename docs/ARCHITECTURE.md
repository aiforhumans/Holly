# Architecture

## Overview

Holly Prompt uses a typed-core design:
- edge nodes accept or emit plain `STRING`
- internal Holly pipeline nodes exchange typed payloads
- inspect nodes expose typed payloads as readable `STRING`

This keeps the graph safe inside Holly while still making the payloads observable and easy to debug.

## Internal Payload Types

- `HOLLY_BUNDLE`
- `HOLLY_INTENT`
- `HOLLY_SEMANTIC_CANDIDATES`
- `HOLLY_VALIDATED_SEMANTICS`
- `HOLLY_STRATEGY`
- `HOLLY_BLUEPRINT`
- `HOLLY_HISTORY_HITS`
- `HOLLY_PROFILE`
- `HOLLY_REUSABLE_PATTERNS`

Each typed payload is a Python `dict` tagged with `_holly_type`. The node layer validates payload type and required keys before doing work.

## Layering

### Prompting layer
- File: `nodes/prompt_nodes.py`
- Purpose: string-based edge utilities for prompt preparation
- Nodes: `Prompt Prefix`, `Prompt + Image Tags`

### Core layer
- Files: `nodes/backbone_nodes.py`, `core/prompt_logic.py`, `core/contracts.py`
- Purpose: typed prompt flow, validation, formatting, strategy, inspect adapters

### Memory layer
- File: `services/history_store.py`
- Purpose: trace persistence, retrieval, preference profiling

## Flow Contracts

### Core prompt flow
- `Holly Input Bundle` -> `HOLLY_BUNDLE`
- `Holly Intent Analyze` -> `HOLLY_INTENT`
- `Holly Semantic Expand` -> `HOLLY_SEMANTIC_CANDIDATES`
- `Holly Integrity Validate` -> `HOLLY_VALIDATED_SEMANTICS`
- `Holly Strategy Select` -> `HOLLY_STRATEGY`
- `Holly Blueprint Build` -> `HOLLY_BLUEPRINT`
- `Holly Model Formatter` -> `STRING`

### Memory flow
- `Holly History Retrieve` -> `HOLLY_HISTORY_HITS`
- `Holly Preference Profile` -> `HOLLY_PROFILE`
- `Holly History Filter` -> `HOLLY_REUSABLE_PATTERNS`

### Inspect/export flow
- Inspect nodes accept one typed Holly payload and output a JSON `STRING`

## Design Constraints

- Preserve the user prompt as the source of truth.
- Keep non-terminal Holly nodes typed so wrong graph links are blocked by ComfyUI.
- Keep inspect/export concerns out of the core transformation nodes.
- Keep storage isolated from prompt logic.

## Compatibility

- `basic_nodes.py` is retained intentionally as a compatibility re-export for older imports.

