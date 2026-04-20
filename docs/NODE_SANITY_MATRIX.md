# Node Sanity Matrix

Status legend:
- `Pass`: nominal behavior works and wrong-contract misuse is blocked or fails loudly.
- `Pass with limits`: behavior is acceptable for the node's role, but the node intentionally remains flexible or has a known design limitation.
- `Fail`: not currently used after the typed-core refactor.

## Prompting

| Node | Category | Inputs | Outputs | Valid Upstream | Valid Downstream | Nominal | Misuse | Edge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Prompt Prefix` | `Holly/Prompting` | `STRING user_prompt`, `STRING prefix`, `BOOLEAN enabled` | `STRING` | None | `Holly Input Bundle` | Pass | Pass with limits | Edge |
| `Prompt + Image Tags` | `Holly/Prompting` | `IMAGE image`, `STRING user_prompt`, `STRING prefix`, `STRING image_tags`, `BOOLEAN enabled` | `STRING` | None | `Holly Input Bundle` | Pass | Pass with limits | Edge |

## Core

| Node | Category | Inputs | Outputs | Valid Upstream | Valid Downstream | Nominal | Misuse | Edge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Holly Input Bundle` | `Holly/Core` | `STRING user_prompt`, `STRING context_block`, `STRING mode`, `STRING target_model`, `STRING user_id`, `BOOLEAN enabled` | `HOLLY_BUNDLE` | `Prompt Prefix`, `Prompt + Image Tags` | `Holly Intent Analyze`, `Holly Integrity Validate`, `Holly Strategy Select`, `Holly Blueprint Build`, `Holly Prompt Compare`, `Holly Trace Save`, `Holly History Retrieve`, `Holly Preference Profile`, `Holly Bundle Inspect` | Pass | Pass with limits | Graph |
| `Holly Intent Analyze` | `Holly/Core` | `HOLLY_BUNDLE raw_bundle` | `HOLLY_INTENT` | `Holly Input Bundle` | `Holly Semantic Expand`, `Holly Strategy Select`, `Holly History Filter`, `Holly Trace Save`, `Holly Intent Inspect` | Pass | Pass | Graph |
| `Holly Semantic Expand` | `Holly/Core` | `HOLLY_INTENT intent_map`, `FLOAT expansion_strength`, optional `HOLLY_REUSABLE_PATTERNS reusable_patterns` | `HOLLY_SEMANTIC_CANDIDATES` | `Holly Intent Analyze`, `Holly History Filter` | `Holly Integrity Validate`, `Holly Semantics Inspect` | Pass | Pass | Graph |
| `Holly Integrity Validate` | `Holly/Core` | `HOLLY_BUNDLE raw_bundle`, `HOLLY_SEMANTIC_CANDIDATES semantic_candidates` | `HOLLY_VALIDATED_SEMANTICS`, `STRING warnings` | `Holly Input Bundle`, `Holly Semantic Expand` | `Holly Strategy Select`, `Holly Blueprint Build`, `Holly Semantics Inspect` | Pass | Pass | Graph |
| `Holly Strategy Select` | `Holly/Core` | `HOLLY_BUNDLE raw_bundle`, `HOLLY_INTENT intent_map`, `HOLLY_VALIDATED_SEMANTICS validated_semantics`, `FLOAT preserve_strength`, optional `HOLLY_PROFILE profile`, optional `HOLLY_REUSABLE_PATTERNS reusable_patterns` | `HOLLY_STRATEGY` | `Holly Input Bundle`, `Holly Intent Analyze`, `Holly Integrity Validate`, `Holly Preference Profile`, `Holly History Filter` | `Holly Blueprint Build`, `Holly Prompt Compare`, `Holly Trace Save`, `Holly Strategy Inspect` | Pass | Pass | Graph |
| `Holly Blueprint Build` | `Holly/Core` | `HOLLY_BUNDLE raw_bundle`, `HOLLY_VALIDATED_SEMANTICS validated_semantics`, `HOLLY_STRATEGY strategy_profile` | `HOLLY_BLUEPRINT` | `Holly Input Bundle`, `Holly Integrity Validate`, `Holly Strategy Select` | `Holly Model Formatter`, `Holly Blueprint Inspect` | Pass | Pass | Graph |
| `Holly Model Formatter` | `Holly/Core` | `HOLLY_BLUEPRINT prompt_blueprint` | `STRING final_prompt` | `Holly Blueprint Build` | `Holly Prompt Compare`, `Holly Trace Save` | Pass | Pass | Terminal |
| `Holly Prompt Compare` | `Holly/Core` | `HOLLY_BUNDLE raw_bundle`, `STRING final_prompt`, `HOLLY_STRATEGY strategy_profile` | `STRING compare_text` | `Holly Input Bundle`, `Holly Model Formatter`, `Holly Strategy Select` | None | Pass | Pass | Terminal |

## Memory

| Node | Category | Inputs | Outputs | Valid Upstream | Valid Downstream | Nominal | Misuse | Edge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Holly Trace Save` | `Holly/Memory` | `HOLLY_BUNDLE raw_bundle`, `HOLLY_INTENT intent_map`, `HOLLY_STRATEGY strategy_profile`, `STRING final_prompt`, `INT score`, `BOOLEAN liked`, `STRING notes` | `STRING trace_id`, `STRING save_status` | `Holly Input Bundle`, `Holly Intent Analyze`, `Holly Strategy Select`, `Holly Model Formatter` | `Holly Session Viewer` | Pass | Pass | Graph |
| `Holly History Retrieve` | `Holly/Memory` | `HOLLY_BUNDLE raw_bundle`, `INT top_k` | `HOLLY_HISTORY_HITS` | `Holly Input Bundle` | `Holly History Filter`, `Holly History Hits Inspect` | Pass | Pass | Graph |
| `Holly Preference Profile` | `Holly/Memory` | `HOLLY_BUNDLE raw_bundle` | `HOLLY_PROFILE` | `Holly Input Bundle` | `Holly Strategy Select`, `Holly Profile Inspect` | Pass | Pass | Graph |
| `Holly History Filter` | `Holly/Memory` | `HOLLY_HISTORY_HITS history_hits`, `HOLLY_INTENT intent_map` | `HOLLY_REUSABLE_PATTERNS` | `Holly History Retrieve`, `Holly Intent Analyze` | `Holly Semantic Expand`, `Holly Strategy Select`, `Holly Reusable Patterns Inspect` | Pass | Pass | Graph |
| `Holly Session Viewer` | `Holly/Memory` | `STRING trace_id` | `STRING session_report` | `Holly Trace Save` | None | Pass | Pass with limits | Terminal |

## Inspect

| Node | Category | Inputs | Outputs | Valid Upstream | Valid Downstream | Nominal | Misuse | Edge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Holly Bundle Inspect` | `Holly/Inspect` | `HOLLY_BUNDLE raw_bundle` | `STRING` | `Holly Input Bundle` | None | Pass | Pass | Inspect |
| `Holly Intent Inspect` | `Holly/Inspect` | `HOLLY_INTENT intent_map` | `STRING` | `Holly Intent Analyze` | None | Pass | Pass | Inspect |
| `Holly Semantics Inspect` | `Holly/Inspect` | optional `HOLLY_SEMANTIC_CANDIDATES semantic_candidates`, optional `HOLLY_VALIDATED_SEMANTICS validated_semantics` | `STRING` | `Holly Semantic Expand`, `Holly Integrity Validate` | None | Pass | Pass | Inspect |
| `Holly Strategy Inspect` | `Holly/Inspect` | `HOLLY_STRATEGY strategy_profile` | `STRING` | `Holly Strategy Select` | None | Pass | Pass | Inspect |
| `Holly Blueprint Inspect` | `Holly/Inspect` | `HOLLY_BLUEPRINT prompt_blueprint` | `STRING` | `Holly Blueprint Build` | None | Pass | Pass | Inspect |
| `Holly History Hits Inspect` | `Holly/Inspect` | `HOLLY_HISTORY_HITS history_hits` | `STRING` | `Holly History Retrieve` | None | Pass | Pass | Inspect |
| `Holly Profile Inspect` | `Holly/Inspect` | `HOLLY_PROFILE profile` | `STRING` | `Holly Preference Profile` | None | Pass | Pass | Inspect |
| `Holly Reusable Patterns Inspect` | `Holly/Inspect` | `HOLLY_REUSABLE_PATTERNS reusable_patterns` | `STRING` | `Holly History Filter` | None | Pass | Pass | Inspect |

