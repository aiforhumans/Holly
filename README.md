# 👼 Holly Prompt

**Advanced prompt orchestration and memory management for ComfyUI**

Holly Prompt is a ComfyUI custom node package providing typed prompt graphs, semantic analysis, strategy selection, and persistent prompt history with local SQLite storage.

## ✨ Features

- **Typed Payload System** – Strongly-typed internal graph flow with payload contracts
- **Semantic Analysis** – Intent detection and semantic expansion for prompt enhancement
- **Strategy Selection** – Multi-strategy prompt composition and validation
- **History & Memory** – SQLite-backed history retrieval, filtering, and preference profiling
- **Blueprint Generation** – Structured prompt blueprint creation and formatting
- **Inspection Tools** – Debug nodes for examining typed payloads as readable JSON
- **Local Storage** – No external API calls; all data stored locally

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Node Categories](#node-categories)
- [Recommended Workflows](#recommended-workflows)
- [Project Structure](#project-structure)
- [Development](#development)
- [Known Limitations](#known-limitations)

## Installation

1. Clone or place this package in your ComfyUI custom_nodes directory:
   ```
   ComfyUI/custom_nodes/Holly_prompt/
   ```

2. Restart ComfyUI

3. Holly nodes will appear in the node menu under:
   - **Holly/Prompting** – Text and image-based prompt utilities
   - **Holly/Core** – Main orchestration and analysis nodes
   - **Holly/Memory** – History and profile management
   - **Holly/Inspect** – Debugging and payload inspection

## Quick Start

1. Add a `Holly Input Bundle` node (Holly/Core)
2. Connect a prompt string input
3. Chain through `Holly Intent Analyze` → `Holly Semantic Expand` → `Holly Strategy Select`
4. Use `Holly Model Formatter` to prepare the final prompt
5. Connect output to your model input

For memory workflows, add `Holly History Retrieve` and `Holly Trace Save` to record and reuse patterns.

## Node Categories

### Holly/Prompting
Edge utility nodes that work with `STRING` payloads:

| Node | Purpose |
|------|---------|
| `Prompt Prefix` | Add custom prefixes to prompts |
| `Prompt + Image Tags` | Combine prompts with image metadata |

### Holly/Core
Main orchestration nodes using typed internal payloads:

| Node | Internal Type | Purpose |
|------|---------------|---------|
| `Holly Input Bundle` | `HOLLY_BUNDLE` | Package input prompt and metadata |
| `Holly Intent Analyze` | `HOLLY_INTENT` | Detect user intent from prompt |
| `Holly Semantic Expand` | `HOLLY_SEMANTIC_CANDIDATES` | Generate semantic variations |
| `Holly Integrity Validate` | `HOLLY_VALIDATED_SEMANTICS` | Validate semantic coherence |
| `Holly Strategy Select` | `HOLLY_STRATEGY` | Select optimal composition strategy |
| `Holly Blueprint Build` | `HOLLY_BLUEPRINT` | Build structured prompt blueprint |
| `Holly Model Formatter` | `STRING` | Format blueprint for model input |
| `Holly Prompt Compare` | Comparison result | Compare prompt variations |

### Holly/Memory
History and preference management:

| Node | Types | Purpose |
|------|-------|---------|
| `Holly Trace Save` | `HOLLY_HISTORY_HITS` | Save prompts and results to history |
| `Holly History Retrieve` | `HOLLY_HISTORY_HITS` | Query historical prompts |
| `Holly History Filter` | `HOLLY_HISTORY_HITS` | Filter history by criteria |
| `Holly Preference Profile` | `HOLLY_PROFILE` | Manage user preferences |
| `Holly Session Viewer` | - | Inspect current session data |

### Holly/Inspect
Debug nodes that expose typed payloads as readable `STRING` JSON:

- `Holly Bundle Inspect`
- `Holly Intent Inspect`
- `Holly Semantics Inspect`
- `Holly Strategy Inspect`
- `Holly Blueprint Inspect`
- `Holly History Hits Inspect`
- `Holly Profile Inspect`
- `Holly Reusable Patterns Inspect`

## Recommended Workflows

### Core Prompt Pipeline
Recommended flow for standard prompt processing:

```
Prompt String
    ↓
[Prompt Prefix] or [Prompt + Image Tags] (optional)
    ↓
[Holly Input Bundle]
    ↓
[Holly Intent Analyze]
    ↓
[Holly Semantic Expand]
    ↓
[Holly Integrity Validate]
    ↓
[Holly Strategy Select]
    ↓
[Holly Blueprint Build]
    ↓
[Holly Model Formatter]
    ↓
[Holly Prompt Compare] (optional, for A/B testing)
    ↓
Model Input
```

### History & Memory Loop
Build and reuse effective prompts:

```
[Holly Input Bundle]
    ↓
[Holly History Retrieve] ← Query past prompts
    ↓
[Holly History Filter]
    ↓
[Holly Semantic Expand] or [Holly Strategy Select]
    ↓
[Holly Trace Save] ← Save new results
    ↓
[Holly Session Viewer] ← Monitor patterns
```

### Debug & Inspection
Use inspect nodes to examine any typed payload:

```
[Any Holly Node] → [Matching Inspect Node] → JSON output
```

For example: `Holly Blueprint Build` → `Holly Blueprint Inspect` to see the blueprint structure.

## Project Structure

```
Holly_prompt/
├── nodes/                    # ComfyUI node implementations
│   ├── prompt_nodes.py       # Prompting category nodes
│   └── backbone_nodes.py     # Core/Memory/Inspect nodes
├── core/                     # Business logic and contracts
│   ├── contracts.py          # Typed payload definitions
│   └── prompt_logic.py       # Orchestration algorithms
├── services/                 # Data persistence
│   └── history_store.py      # SQLite history backend
├── data/                     # Database storage
│   └── holly_prompt.db       # Default history database
├── tests/                    # Test suite
│   ├── test_*.py             # Unit tests
│   └── sanity_harness.py     # Node registration validator
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # System design
│   ├── NODE_MAP.md           # Node reference
│   └── NODE_SANITY_MATRIX.md # Validation matrix
├── pyproject.toml            # Python package config
├── LICENSE                   # License file
└── README.md                 # This file
```

## Storage

Prompt history and profiles are stored locally in SQLite:

```
Holly_prompt/data/holly_prompt.db
```

To override the database path (useful for testing or external tooling):

```python
import os
os.environ['HOLLY_PROMPT_DB_PATH'] = '/custom/path/holly.db'
```

## Development

### Running Tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

### Test Coverage

- `test_prompt_logic.py` – Core orchestration logic
- `test_history_store.py` – Database operations
- `test_node_sanity.py` – Node registration and signatures
- `test_registration.py` – ComfyUI integration
- `sanity_harness.py` – Full node validation harness

### Backward Compatibility

`basic_nodes.py` is retained as a backward-compatible re-export of the `Holly/Prompting` node utility classes.

## Known Limitations

- **Image Analysis** – `Prompt + Image Tags` requires an image input but doesn't analyze tensor content
- **Intent & Strategy** – Analysis is heuristic-based, not LLM-driven
- **History Search** – Uses token overlap for retrieval, not embeddings or semantic similarity
- **Model Configuration** – `mode` and `target_model` are free-form widget strings at bundle entry point
- **No External APIs** – All processing is local; no cloud dependencies

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Nodes don't appear in menu | Restart ComfyUI; check console for import errors |
| Database errors | Verify write permissions to `data/` directory |
| History not saving | Check `HOLLY_PROMPT_DB_PATH` environment variable |
| Type mismatches in graph | Use inspect nodes to verify payload structure |

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) – System design and data flow
- [NODE_MAP.md](docs/NODE_MAP.md) – Complete node reference
- [NODE_SANITY_MATRIX.md](docs/NODE_SANITY_MATRIX.md) – Test coverage matrix
- [CHANGELOG.md](docs/CHANGELOG.md) – Version history

## License

See [LICENSE](LICENSE) file for details.

