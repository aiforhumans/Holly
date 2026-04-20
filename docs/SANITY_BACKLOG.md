# Sanity Backlog

This backlog covers residual work after the typed-core refactor and final node sanity pass.

## P0

### Broken
- None. The typed-core chain, inspect adapters, and memory loop all pass nominal execution and wrong-contract misuse checks.

### Works With Structural Risk
- None at P0. Wrong stage-to-stage links inside the Holly core are now blocked by typed payloads instead of falling through as generic `STRING`.

### Missing Counterpart
- None. Every non-edge Holly payload type has at least one valid upstream producer and one valid downstream consumer, plus an inspect node where appropriate.

### Optimization
- None at P0.

## P1

### Broken
- None currently reproduced by the sanity harness or live registry verification.

### Works With Structural Risk
- `Prompt + Image Tags`
  - The `IMAGE` input is structural only. The node guarantees graph placement and tag-merging, but it does not inspect the image tensor or validate that `image_tags` actually came from that image.
- `Holly Input Bundle`
  - `mode` and `target_model` are still free-form edge strings. The typed-core flow prevents downstream drift, but the bundle edge does not yet constrain invalid UI values.
- `Holly Session Viewer`
  - `trace_id` remains a plain `STRING`. Wrong IDs are handled safely (`Trace not found.`), but failure is still runtime lookup rather than typed linkage.

### Missing Counterpart
- None.

### Optimization
- Add widget-level `COMBO` options or validated enums for `mode` and common `target_model` values if the workflow should be more guided.
- Add a dedicated export node family if typed Holly payloads need to leave the Holly graph for non-Holly consumers in a more structured way than inspect nodes.

## P2

### Broken
- None.

### Works With Structural Risk
- `Holly Intent Analyze`
  - Intent extraction is heuristic and vocabulary-limited. It is structurally correct now, but semantically shallow.
- `Holly Semantic Expand`
  - Optional history reuse currently injects prior patterns conservatively but still relies on simple string reuse, not semantic decomposition.
- `Holly Strategy Select`
  - Profile influence is intentionally light (`preferred_mode`, reuse count). It does not yet learn richer prompting preferences.
- `Prompt Prefix`
  - Generic `STRING` edge utility by design. It is valid upstream to `Holly Input Bundle`, but it is not a typed Holly stage.

### Missing Counterpart
- None.

### Optimization
- Replace token-overlap retrieval in `Holly History Retrieve` with embeddings or richer subject/action/setting indexing.
- Add a schema-version field to typed Holly payloads if backward compatibility across future node revisions matters.
- Add richer inspect formatting (field grouping, diff views, truncation controls) instead of raw JSON dumps.
- Expand the sanity harness to score output quality heuristics, not just contract correctness and failure behavior.

