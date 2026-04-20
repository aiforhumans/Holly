HOLLY_BUNDLE = "HOLLY_BUNDLE"
HOLLY_INTENT = "HOLLY_INTENT"
HOLLY_SEMANTIC_CANDIDATES = "HOLLY_SEMANTIC_CANDIDATES"
HOLLY_VALIDATED_SEMANTICS = "HOLLY_VALIDATED_SEMANTICS"
HOLLY_STRATEGY = "HOLLY_STRATEGY"
HOLLY_BLUEPRINT = "HOLLY_BLUEPRINT"
HOLLY_HISTORY_HITS = "HOLLY_HISTORY_HITS"
HOLLY_PROFILE = "HOLLY_PROFILE"
HOLLY_REUSABLE_PATTERNS = "HOLLY_REUSABLE_PATTERNS"

TYPE_FIELD = "_holly_type"

MAPPING_REQUIRED_KEYS = {
    HOLLY_BUNDLE: (
        "timestamp",
        "user_prompt",
        "context_block",
        "mode",
        "target_model",
        "user_id",
    ),
    HOLLY_INTENT: (
        "subject",
        "action",
        "setting",
        "style",
        "composition",
        "mood",
        "confidence",
    ),
    HOLLY_SEMANTIC_CANDIDATES: (
        "subject_details",
        "action_details",
        "environment_details",
        "style_details",
        "history_hints",
        "rejected",
    ),
    HOLLY_VALIDATED_SEMANTICS: (
        "subject_details",
        "action_details",
        "environment_details",
        "style_details",
        "history_hints",
        "rejected",
    ),
    HOLLY_STRATEGY: (
        "mode",
        "preserve_strength",
        "expansion_strength",
        "format_type",
        "target_model",
        "intent_confidence",
        "history_reuse_count",
    ),
    HOLLY_BLUEPRINT: (
        "core",
        "supporting",
        "context",
        "mode",
        "format_type",
        "target_model",
        "user_id",
    ),
    HOLLY_HISTORY_HITS: ("items",),
    HOLLY_PROFILE: (
        "user_id",
        "prompt_count",
        "avg_score",
        "liked_ratio",
        "preferred_mode",
    ),
    HOLLY_REUSABLE_PATTERNS: ("items",),
}


def make_payload(payload_type, **data):
    payload = {TYPE_FIELD: payload_type}
    payload.update(data)
    return payload


def require_payload(payload, payload_type):
    if not isinstance(payload, dict):
        raise TypeError(f"{payload_type} payload must be a dict, got {type(payload).__name__}")

    actual_type = payload.get(TYPE_FIELD)
    if actual_type != payload_type:
        raise ValueError(f"Expected {payload_type} payload, got {actual_type or 'untyped payload'}")

    missing = [key for key in MAPPING_REQUIRED_KEYS.get(payload_type, ()) if key not in payload]
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"{payload_type} payload missing required keys: {missing_text}")

    return payload


def require_items_payload(payload, payload_type):
    payload = require_payload(payload, payload_type)
    items = payload.get("items")
    if not isinstance(items, list):
        raise TypeError(f"{payload_type}.items must be a list")
    return payload

