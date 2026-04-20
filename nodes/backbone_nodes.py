from ..core.contracts import (
    HOLLY_BLUEPRINT,
    HOLLY_BUNDLE,
    HOLLY_HISTORY_HITS,
    HOLLY_INTENT,
    HOLLY_PROFILE,
    HOLLY_REUSABLE_PATTERNS,
    HOLLY_SEMANTIC_CANDIDATES,
    HOLLY_STRATEGY,
    HOLLY_VALIDATED_SEMANTICS,
    require_items_payload,
    require_payload,
)
from ..core.prompt_logic import (
    analyze_intent,
    build_blueprint,
    build_compare_text,
    expand_semantics,
    filter_reusable_patterns,
    format_model_prompt,
    normalize_bundle,
    select_strategy,
    to_json,
    validate_semantics,
    wrap_history_hits,
    wrap_profile,
)
from ..services.history_store import get_profile, get_trace, retrieve_similar, save_trace


class HollyInputBundleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"default": "", "multiline": True}),
                "context_block": ("STRING", {"default": "", "multiline": True}),
                "mode": ("STRING", {"default": "auto"}),
                "target_model": ("STRING", {"default": "z-image-turbo"}),
                "user_id": ("STRING", {"default": "default"}),
                "enabled": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (HOLLY_BUNDLE,)
    RETURN_NAMES = ("raw_bundle",)
    FUNCTION = "build_bundle"
    CATEGORY = "Holly/Core"

    def build_bundle(self, user_prompt, context_block, mode, target_model, user_id, enabled):
        if not enabled:
            return (
                normalize_bundle(
                    user_prompt=user_prompt,
                    context_block=context_block,
                    mode="preserve",
                    target_model=target_model,
                    user_id=user_id,
                ),
            )
        return (normalize_bundle(user_prompt, context_block, mode, target_model, user_id),)


class HollyIntentAnalyzeNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"raw_bundle": (HOLLY_BUNDLE,)}} 

    RETURN_TYPES = (HOLLY_INTENT,)
    RETURN_NAMES = ("intent_map",)
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, raw_bundle):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        return (analyze_intent(bundle),)


class HollySemanticExpandNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "intent_map": (HOLLY_INTENT,),
                "expansion_strength": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.05}),
            },
            "optional": {
                "reusable_patterns": (HOLLY_REUSABLE_PATTERNS,),
            },
        }

    RETURN_TYPES = (HOLLY_SEMANTIC_CANDIDATES,)
    RETURN_NAMES = ("semantic_candidates",)
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, intent_map, expansion_strength, reusable_patterns=None):
        intent = require_payload(intent_map, HOLLY_INTENT)
        patterns = None
        if reusable_patterns is not None:
            patterns = require_items_payload(reusable_patterns, HOLLY_REUSABLE_PATTERNS)
        return (expand_semantics(intent, expansion_strength, patterns),)


class HollyIntegrityValidateNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_bundle": (HOLLY_BUNDLE,),
                "semantic_candidates": (HOLLY_SEMANTIC_CANDIDATES,),
            }
        }

    RETURN_TYPES = (HOLLY_VALIDATED_SEMANTICS, "STRING")
    RETURN_NAMES = ("validated_semantics", "warnings")
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, raw_bundle, semantic_candidates):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        candidates = require_payload(semantic_candidates, HOLLY_SEMANTIC_CANDIDATES)
        validated, warnings = validate_semantics(bundle, candidates)
        return (validated, "\n".join(warnings).strip())


class HollyStrategySelectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_bundle": (HOLLY_BUNDLE,),
                "intent_map": (HOLLY_INTENT,),
                "validated_semantics": (HOLLY_VALIDATED_SEMANTICS,),
                "preserve_strength": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.05}),
            },
            "optional": {
                "profile": (HOLLY_PROFILE,),
                "reusable_patterns": (HOLLY_REUSABLE_PATTERNS,),
            },
        }

    RETURN_TYPES = (HOLLY_STRATEGY,)
    RETURN_NAMES = ("strategy_profile",)
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, raw_bundle, intent_map, validated_semantics, preserve_strength, profile=None, reusable_patterns=None):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        intent = require_payload(intent_map, HOLLY_INTENT)
        validated = require_payload(validated_semantics, HOLLY_VALIDATED_SEMANTICS)
        typed_profile = None
        typed_patterns = None
        if profile is not None:
            typed_profile = require_payload(profile, HOLLY_PROFILE)
        if reusable_patterns is not None:
            typed_patterns = require_items_payload(reusable_patterns, HOLLY_REUSABLE_PATTERNS)
        return (select_strategy(bundle, intent, validated, preserve_strength, typed_profile, typed_patterns),)


class HollyBlueprintBuildNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_bundle": (HOLLY_BUNDLE,),
                "validated_semantics": (HOLLY_VALIDATED_SEMANTICS,),
                "strategy_profile": (HOLLY_STRATEGY,),
            }
        }

    RETURN_TYPES = (HOLLY_BLUEPRINT,)
    RETURN_NAMES = ("prompt_blueprint",)
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, raw_bundle, validated_semantics, strategy_profile):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        validated = require_payload(validated_semantics, HOLLY_VALIDATED_SEMANTICS)
        strategy = require_payload(strategy_profile, HOLLY_STRATEGY)
        return (build_blueprint(bundle, validated, strategy),)


class HollyModelFormatterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"prompt_blueprint": (HOLLY_BLUEPRINT,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, prompt_blueprint):
        blueprint = require_payload(prompt_blueprint, HOLLY_BLUEPRINT)
        return (format_model_prompt(blueprint),)


class HollyPromptCompareNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_bundle": (HOLLY_BUNDLE,),
                "final_prompt": ("STRING", {"default": "", "multiline": True}),
                "strategy_profile": (HOLLY_STRATEGY,),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("compare_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Core"

    def run(self, raw_bundle, final_prompt, strategy_profile):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        strategy = require_payload(strategy_profile, HOLLY_STRATEGY)
        return (build_compare_text(bundle, final_prompt, strategy),)


class HollyTraceSaveNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_bundle": (HOLLY_BUNDLE,),
                "intent_map": (HOLLY_INTENT,),
                "strategy_profile": (HOLLY_STRATEGY,),
                "final_prompt": ("STRING", {"default": "", "multiline": True}),
                "score": ("INT", {"default": 0, "min": 0, "max": 5}),
                "liked": ("BOOLEAN", {"default": False}),
                "notes": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("trace_id", "save_status")
    FUNCTION = "run"
    CATEGORY = "Holly/Memory"

    def run(self, raw_bundle, intent_map, strategy_profile, final_prompt, score, liked, notes):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        intent = require_payload(intent_map, HOLLY_INTENT)
        strategy = require_payload(strategy_profile, HOLLY_STRATEGY)
        trace_id, profile = save_trace(
            {
                "user_id": bundle["user_id"],
                "raw_prompt": bundle["user_prompt"],
                "final_prompt": final_prompt,
                "target_model": bundle["target_model"],
                "intent_map": intent,
                "strategy_profile": strategy,
                "score": score,
                "liked": liked,
                "notes": notes,
            }
        )
        status = f"Saved trace {trace_id}. Prompt count: {profile.get('prompt_count', 0)}"
        return (trace_id, status)


class HollyHistoryRetrieveNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_bundle": (HOLLY_BUNDLE,),
                "top_k": ("INT", {"default": 5, "min": 1, "max": 20}),
            }
        }

    RETURN_TYPES = (HOLLY_HISTORY_HITS,)
    RETURN_NAMES = ("history_hits",)
    FUNCTION = "run"
    CATEGORY = "Holly/Memory"

    def run(self, raw_bundle, top_k):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        hits = retrieve_similar(bundle["user_prompt"], top_k=top_k, user_id=bundle["user_id"])
        return (wrap_history_hits(hits),)


class HollyPreferenceProfileNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"raw_bundle": (HOLLY_BUNDLE,)}} 

    RETURN_TYPES = (HOLLY_PROFILE,)
    RETURN_NAMES = ("profile",)
    FUNCTION = "run"
    CATEGORY = "Holly/Memory"

    def run(self, raw_bundle):
        bundle = require_payload(raw_bundle, HOLLY_BUNDLE)
        return (wrap_profile(get_profile(bundle["user_id"])),)


class HollyHistoryFilterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "history_hits": (HOLLY_HISTORY_HITS,),
                "intent_map": (HOLLY_INTENT,),
            }
        }

    RETURN_TYPES = (HOLLY_REUSABLE_PATTERNS,)
    RETURN_NAMES = ("reusable_patterns",)
    FUNCTION = "run"
    CATEGORY = "Holly/Memory"

    def run(self, history_hits, intent_map):
        hits = require_items_payload(history_hits, HOLLY_HISTORY_HITS)
        intent = require_payload(intent_map, HOLLY_INTENT)
        return (filter_reusable_patterns(hits, intent),)


class HollySessionViewerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"trace_id": ("STRING", {"default": ""})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("session_report",)
    FUNCTION = "run"
    CATEGORY = "Holly/Memory"

    def run(self, trace_id):
        trace = get_trace(trace_id.strip())
        if not trace:
            return ("Trace not found.",)
        return (to_json(trace),)


class HollyBundleInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"raw_bundle": (HOLLY_BUNDLE,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("bundle_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, raw_bundle):
        return (to_json(require_payload(raw_bundle, HOLLY_BUNDLE)),)


class HollyIntentInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"intent_map": (HOLLY_INTENT,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("intent_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, intent_map):
        return (to_json(require_payload(intent_map, HOLLY_INTENT)),)


class HollySemanticsInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "semantic_candidates": (HOLLY_SEMANTIC_CANDIDATES,),
                "validated_semantics": (HOLLY_VALIDATED_SEMANTICS,),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("semantics_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, semantic_candidates=None, validated_semantics=None):
        if semantic_candidates is not None:
            return (to_json(require_payload(semantic_candidates, HOLLY_SEMANTIC_CANDIDATES)),)
        if validated_semantics is not None:
            return (to_json(require_payload(validated_semantics, HOLLY_VALIDATED_SEMANTICS)),)
        raise ValueError("HollySemanticsInspectNode requires semantic_candidates or validated_semantics")


class HollyStrategyInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"strategy_profile": (HOLLY_STRATEGY,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("strategy_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, strategy_profile):
        return (to_json(require_payload(strategy_profile, HOLLY_STRATEGY)),)


class HollyBlueprintInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"prompt_blueprint": (HOLLY_BLUEPRINT,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("blueprint_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, prompt_blueprint):
        return (to_json(require_payload(prompt_blueprint, HOLLY_BLUEPRINT)),)


class HollyHistoryHitsInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"history_hits": (HOLLY_HISTORY_HITS,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("history_hits_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, history_hits):
        return (to_json(require_items_payload(history_hits, HOLLY_HISTORY_HITS)),)


class HollyProfileInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"profile": (HOLLY_PROFILE,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("profile_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, profile):
        return (to_json(require_payload(profile, HOLLY_PROFILE)),)


class HollyReusablePatternsInspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"reusable_patterns": (HOLLY_REUSABLE_PATTERNS,)}} 

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("reusable_patterns_text",)
    FUNCTION = "run"
    CATEGORY = "Holly/Inspect"

    def run(self, reusable_patterns):
        return (to_json(require_items_payload(reusable_patterns, HOLLY_REUSABLE_PATTERNS)),)

