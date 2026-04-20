# Node Map

## Prompting

- `Prompt Prefix`
  - Inputs: `STRING user_prompt`, `STRING prefix`, `BOOLEAN enabled`
  - Output: `STRING final_prompt`
  - Intended downstream: `Holly Input Bundle`

- `Prompt + Image Tags`
  - Inputs: `IMAGE image`, `STRING user_prompt`, `STRING prefix`, `STRING image_tags`, `BOOLEAN enabled`
  - Output: `STRING final_prompt`
  - Intended downstream: `Holly Input Bundle`

## Core

- `Holly Input Bundle`
  - Inputs: edge `STRING` values for prompt/context/mode/model/user
  - Output: `HOLLY_BUNDLE`

- `Holly Intent Analyze`
  - Input: `HOLLY_BUNDLE`
  - Output: `HOLLY_INTENT`

- `Holly Semantic Expand`
  - Input: `HOLLY_INTENT`
  - Optional input: `HOLLY_REUSABLE_PATTERNS`
  - Output: `HOLLY_SEMANTIC_CANDIDATES`

- `Holly Integrity Validate`
  - Inputs: `HOLLY_BUNDLE`, `HOLLY_SEMANTIC_CANDIDATES`
  - Outputs: `HOLLY_VALIDATED_SEMANTICS`, `STRING warnings`

- `Holly Strategy Select`
  - Inputs: `HOLLY_BUNDLE`, `HOLLY_INTENT`, `HOLLY_VALIDATED_SEMANTICS`
  - Optional inputs: `HOLLY_PROFILE`, `HOLLY_REUSABLE_PATTERNS`
  - Output: `HOLLY_STRATEGY`

- `Holly Blueprint Build`
  - Inputs: `HOLLY_BUNDLE`, `HOLLY_VALIDATED_SEMANTICS`, `HOLLY_STRATEGY`
  - Output: `HOLLY_BLUEPRINT`

- `Holly Model Formatter`
  - Input: `HOLLY_BLUEPRINT`
  - Output: `STRING final_prompt`

- `Holly Prompt Compare`
  - Inputs: `HOLLY_BUNDLE`, `STRING final_prompt`, `HOLLY_STRATEGY`
  - Output: `STRING compare_text`

## Memory

- `Holly Trace Save`
  - Inputs: `HOLLY_BUNDLE`, `HOLLY_INTENT`, `HOLLY_STRATEGY`, `STRING final_prompt`, `INT score`, `BOOLEAN liked`, `STRING notes`
  - Outputs: `STRING trace_id`, `STRING save_status`

- `Holly History Retrieve`
  - Inputs: `HOLLY_BUNDLE`, `INT top_k`
  - Output: `HOLLY_HISTORY_HITS`

- `Holly Preference Profile`
  - Input: `HOLLY_BUNDLE`
  - Output: `HOLLY_PROFILE`

- `Holly History Filter`
  - Inputs: `HOLLY_HISTORY_HITS`, `HOLLY_INTENT`
  - Output: `HOLLY_REUSABLE_PATTERNS`

- `Holly Session Viewer`
  - Input: `STRING trace_id`
  - Output: `STRING session_report`

## Inspect

- `Holly Bundle Inspect`
  - Input: `HOLLY_BUNDLE`
  - Output: `STRING`

- `Holly Intent Inspect`
  - Input: `HOLLY_INTENT`
  - Output: `STRING`

- `Holly Semantics Inspect`
  - Input: `HOLLY_SEMANTIC_CANDIDATES` or `HOLLY_VALIDATED_SEMANTICS`
  - Output: `STRING`

- `Holly Strategy Inspect`
  - Input: `HOLLY_STRATEGY`
  - Output: `STRING`

- `Holly Blueprint Inspect`
  - Input: `HOLLY_BLUEPRINT`
  - Output: `STRING`

- `Holly History Hits Inspect`
  - Input: `HOLLY_HISTORY_HITS`
  - Output: `STRING`

- `Holly Profile Inspect`
  - Input: `HOLLY_PROFILE`
  - Output: `STRING`

- `Holly Reusable Patterns Inspect`
  - Input: `HOLLY_REUSABLE_PATTERNS`
  - Output: `STRING`

