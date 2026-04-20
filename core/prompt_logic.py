import json
import re
from datetime import datetime, timezone

from .contracts import make_payload


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def to_json(data):
    return json.dumps(data, ensure_ascii=True, indent=2)


def parse_json_or_text(value, fallback_key="text"):
    if value is None:
        return {}
    if isinstance(value, (dict, list)):
        return value
    text = str(value).strip()
    if not text:
        return {}
    try:
        parsed = json.loads(text)
        if isinstance(parsed, (dict, list)):
            return parsed
    except Exception:
        pass
    return {fallback_key: text}


def normalize_bundle(user_prompt, context_block, mode, target_model, user_id):
    return make_payload(
        "HOLLY_BUNDLE",
        timestamp=now_iso(),
        user_prompt=(user_prompt or "").strip(),
        context_block=(context_block or "").strip(),
        mode=(mode or "auto").strip().lower(),
        target_model=(target_model or "z-image-turbo").strip(),
        user_id=(user_id or "default").strip(),
    )


def _find_keyword(text, keywords):
    lowered = text.lower()
    for keyword in keywords:
        if keyword in lowered:
            return keyword
    return ""


def analyze_intent(bundle):
    prompt = (bundle.get("user_prompt") or "").strip()
    prompt_lower = prompt.lower()

    subject = prompt
    action = ""
    setting = ""

    match = re.split(r"\bin\b", prompt, maxsplit=1, flags=re.IGNORECASE)
    if len(match) == 2:
        before, after = match
        subject = before.strip()
        setting = after.strip()

    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]*", prompt_lower)
    action_candidates = [word for word in words if word.endswith("ing")]
    if action_candidates:
        action = action_candidates[0]

    style = _find_keyword(
        prompt,
        (
            "cinematic",
            "photoreal",
            "photo",
            "illustration",
            "anime",
            "3d",
            "oil painting",
            "watercolor",
            "concept art",
        ),
    )
    composition = _find_keyword(
        prompt,
        (
            "portrait",
            "full body",
            "close-up",
            "wide shot",
            "macro",
            "overhead",
            "side view",
        ),
    )
    mood = _find_keyword(
        prompt,
        (
            "playful",
            "dramatic",
            "dark",
            "moody",
            "happy",
            "calm",
            "epic",
            "mysterious",
        ),
    )

    confidence = 0.4
    if subject:
        confidence += 0.2
    if action:
        confidence += 0.15
    if setting:
        confidence += 0.15
    if style:
        confidence += 0.1

    return make_payload(
        "HOLLY_INTENT",
        subject=subject,
        action=action,
        setting=setting,
        style=style,
        composition=composition,
        mood=mood,
        confidence=min(confidence, 0.99),
    )


def expand_semantics(intent_map, expansion_strength, reusable_patterns=None):
    strength = max(0.0, min(float(expansion_strength), 1.0))
    subject = intent_map.get("subject", "")
    action = intent_map.get("action", "")
    setting = intent_map.get("setting", "")
    mood = intent_map.get("mood", "")
    style = intent_map.get("style", "")

    details = {
        "subject_details": [],
        "action_details": [],
        "environment_details": [],
        "style_details": [],
        "history_hints": [],
        "rejected": [],
    }

    if subject:
        details["subject_details"].append("clear subject identity and readable silhouette")
    if action:
        details["action_details"].append("motion clarity and pose readability")
    if setting:
        details["environment_details"].append("environment cues consistent with setting")
    if mood:
        details["style_details"].append(f"tone consistent with {mood}")
    if style:
        details["style_details"].append(f"visual style bias toward {style}")

    if strength >= 0.35:
        details["environment_details"].append("coherent foreground and background separation")
    if strength >= 0.6:
        details["style_details"].append("balanced lighting and contrast hierarchy")
    if strength >= 0.8:
        details["action_details"].append("micro-details that support storytelling without noise")

    items = []
    if isinstance(reusable_patterns, dict):
        items = reusable_patterns.get("items", [])
    elif isinstance(reusable_patterns, list):
        items = reusable_patterns

    for item in items[:2]:
        pattern = (item.get("pattern") or "").strip()
        if pattern:
            details["history_hints"].append(pattern)

    if items:
        details["rejected"].append(f"Loaded {len(items)} reusable history pattern(s)")

    return make_payload("HOLLY_SEMANTIC_CANDIDATES", **details)


def validate_semantics(raw_bundle, semantic_candidates):
    user_prompt = (raw_bundle.get("user_prompt") or "").lower()
    cleaned = {
        "subject_details": [],
        "action_details": [],
        "environment_details": [],
        "style_details": [],
        "history_hints": [],
        "rejected": [],
    }
    warnings = []

    seen = set()
    for key in ("subject_details", "action_details", "environment_details", "style_details", "history_hints"):
        for item in semantic_candidates.get(key, []):
            text = (item or "").strip()
            if not text:
                continue
            lowered = text.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            if "ultra detailed" in lowered and "ultra detailed" in user_prompt:
                warnings.append("Removed repeated detail phrase.")
                continue
            cleaned[key].append(text)

    for item in semantic_candidates.get("rejected", []):
        if str(item).strip():
            cleaned["rejected"].append(str(item).strip())

    if not any(cleaned[key] for key in ("subject_details", "action_details", "environment_details", "style_details", "history_hints")):
        warnings.append("No semantic enrichments retained; prompt will stay close to input.")

    return make_payload("HOLLY_VALIDATED_SEMANTICS", **cleaned), warnings


def select_strategy(raw_bundle, intent_map, validated_semantics, preserve_strength, profile=None, reusable_patterns=None):
    mode = (raw_bundle.get("mode") or "auto").lower()
    preserve = max(0.0, min(float(preserve_strength), 1.0))
    detail_count = sum(
        len(validated_semantics.get(key, []))
        for key in ("subject_details", "action_details", "environment_details", "style_details", "history_hints")
    )

    reusable_items = []
    if isinstance(reusable_patterns, dict):
        reusable_items = reusable_patterns.get("items", [])
    elif isinstance(reusable_patterns, list):
        reusable_items = reusable_patterns

    preferred_mode = ""
    if isinstance(profile, dict):
        preferred_mode = (profile.get("preferred_mode") or "").strip().lower()

    if mode == "auto":
        if preferred_mode in {"preserve", "enhance"}:
            mode = preferred_mode
        else:
            mode = "preserve" if detail_count == 0 else "enhance"

    format_type = "generic_sentence"
    model_lower = (raw_bundle.get("target_model") or "").lower()
    if "z-image" in model_lower:
        format_type = "zimage_sentence"
    elif "flux" in model_lower:
        format_type = "flux_dense"
    elif "sdxl" in model_lower:
        format_type = "sdxl_balanced"

    return make_payload(
        "HOLLY_STRATEGY",
        mode=mode,
        preserve_strength=preserve,
        expansion_strength=1.0 - preserve,
        format_type=format_type,
        target_model=raw_bundle.get("target_model", ""),
        intent_confidence=intent_map.get("confidence", 0.0),
        history_reuse_count=len(reusable_items),
    )


def build_blueprint(raw_bundle, validated_semantics, strategy_profile):
    prompt = (raw_bundle.get("user_prompt") or "").strip()
    context_block = (raw_bundle.get("context_block") or "").strip()

    supporting = []
    for key in ("subject_details", "action_details", "environment_details", "style_details", "history_hints"):
        supporting.extend(validated_semantics.get(key, []))

    return make_payload(
        "HOLLY_BLUEPRINT",
        core=prompt,
        supporting=supporting,
        context=context_block,
        mode=strategy_profile.get("mode", "preserve"),
        format_type=strategy_profile.get("format_type", "generic_sentence"),
        target_model=strategy_profile.get("target_model", raw_bundle.get("target_model", "")),
        user_id=raw_bundle.get("user_id", "default"),
    )


def format_model_prompt(prompt_blueprint):
    core = (prompt_blueprint.get("core") or "").strip()
    supporting = [item.strip() for item in prompt_blueprint.get("supporting", []) if str(item).strip()]
    context = (prompt_blueprint.get("context") or "").strip()
    model_lower = (prompt_blueprint.get("target_model") or "").lower()

    parts = []
    if context:
        parts.append(context)
    if core:
        parts.append(core)
    parts.extend(supporting)

    if "flux" in model_lower:
        return ", ".join(parts).strip(" ,")
    if "z-image" in model_lower:
        return ". ".join([part.rstrip(".") for part in parts if part]).strip()
    return "\n".join(parts).strip()


def build_compare_text(raw_bundle, final_prompt, strategy_profile):
    return (
        "Holly Prompt Compare\n"
        f"- Mode: {strategy_profile.get('mode', 'unknown')}\n"
        f"- Format: {strategy_profile.get('format_type', 'unknown')}\n"
        f"- Target Model: {strategy_profile.get('target_model', 'unknown')}\n\n"
        "Original Prompt:\n"
        f"{raw_bundle.get('user_prompt', '')}\n\n"
        "Final Prompt:\n"
        f"{final_prompt}"
    )


def wrap_history_hits(items):
    return make_payload("HOLLY_HISTORY_HITS", items=items)


def wrap_profile(profile):
    return make_payload(
        "HOLLY_PROFILE",
        user_id=profile.get("user_id", "default"),
        prompt_count=profile.get("prompt_count", 0),
        avg_score=profile.get("avg_score", 0.0),
        liked_ratio=profile.get("liked_ratio", 0.0),
        preferred_mode=profile.get("preferred_mode", "enhance"),
    )


def filter_reusable_patterns(history_hits, intent_map):
    subject = (intent_map.get("subject") or "").lower()
    items = []
    if isinstance(history_hits, dict):
        items = history_hits.get("items", [])
    elif isinstance(history_hits, list):
        items = history_hits

    reusable = []
    for hit in items:
        final_prompt = (hit.get("final_prompt") or "").strip()
        if not final_prompt:
            continue
        if subject and subject in final_prompt.lower():
            reusable.append(
                {
                    "trace_id": hit.get("trace_id", ""),
                    "pattern": final_prompt,
                    "reason": "subject overlap",
                }
            )
        elif not subject:
            reusable.append(
                {
                    "trace_id": hit.get("trace_id", ""),
                    "pattern": final_prompt,
                    "reason": "general reusable structure",
                }
            )

    return make_payload("HOLLY_REUSABLE_PATTERNS", items=reusable[:5])

