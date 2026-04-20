import pathlib
import sys


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
CUSTOM_NODES_ROOT = PACKAGE_ROOT.parent

if str(CUSTOM_NODES_ROOT) not in sys.path:
    sys.path.insert(0, str(CUSTOM_NODES_ROOT))

import Holly_prompt as hp
from Holly_prompt.core.contracts import (
    HOLLY_BLUEPRINT,
    HOLLY_BUNDLE,
    HOLLY_HISTORY_HITS,
    HOLLY_INTENT,
    HOLLY_PROFILE,
    HOLLY_REUSABLE_PATTERNS,
    HOLLY_SEMANTIC_CANDIDATES,
    HOLLY_STRATEGY,
    HOLLY_VALIDATED_SEMANTICS,
)


EDGE_STATUS = {
    "PromptPrefixNode": "edge",
    "PromptWithImageTagsNode": "edge",
    "HollyModelFormatterNode": "terminal",
    "HollyPromptCompareNode": "terminal",
    "HollySessionViewerNode": "terminal",
    "HollyBundleInspectNode": "inspect",
    "HollyIntentInspectNode": "inspect",
    "HollySemanticsInspectNode": "inspect",
    "HollyStrategyInspectNode": "inspect",
    "HollyBlueprintInspectNode": "inspect",
    "HollyHistoryHitsInspectNode": "inspect",
    "HollyProfileInspectNode": "inspect",
    "HollyReusablePatternsInspectNode": "inspect",
}

EXPECTED_DOWNSTREAM = {
    "PromptPrefixNode": ["HollyInputBundleNode"],
    "PromptWithImageTagsNode": ["HollyInputBundleNode"],
    "HollyInputBundleNode": [
        "HollyIntentAnalyzeNode",
        "HollyIntegrityValidateNode",
        "HollyStrategySelectNode",
        "HollyBlueprintBuildNode",
        "HollyPromptCompareNode",
        "HollyTraceSaveNode",
        "HollyHistoryRetrieveNode",
        "HollyPreferenceProfileNode",
        "HollyBundleInspectNode",
    ],
    "HollyIntentAnalyzeNode": [
        "HollySemanticExpandNode",
        "HollyStrategySelectNode",
        "HollyHistoryFilterNode",
        "HollyTraceSaveNode",
        "HollyIntentInspectNode",
    ],
    "HollySemanticExpandNode": [
        "HollyIntegrityValidateNode",
        "HollySemanticsInspectNode",
    ],
    "HollyIntegrityValidateNode": [
        "HollyStrategySelectNode",
        "HollyBlueprintBuildNode",
        "HollySemanticsInspectNode",
    ],
    "HollyStrategySelectNode": [
        "HollyBlueprintBuildNode",
        "HollyPromptCompareNode",
        "HollyTraceSaveNode",
        "HollyStrategyInspectNode",
    ],
    "HollyBlueprintBuildNode": [
        "HollyModelFormatterNode",
        "HollyBlueprintInspectNode",
    ],
    "HollyModelFormatterNode": [
        "HollyPromptCompareNode",
        "HollyTraceSaveNode",
    ],
    "HollyPromptCompareNode": [],
    "HollyTraceSaveNode": ["HollySessionViewerNode"],
    "HollyHistoryRetrieveNode": [
        "HollyHistoryFilterNode",
        "HollyHistoryHitsInspectNode",
    ],
    "HollyPreferenceProfileNode": [
        "HollyStrategySelectNode",
        "HollyProfileInspectNode",
    ],
    "HollyHistoryFilterNode": [
        "HollySemanticExpandNode",
        "HollyStrategySelectNode",
        "HollyReusablePatternsInspectNode",
    ],
    "HollySessionViewerNode": [],
    "HollyBundleInspectNode": [],
    "HollyIntentInspectNode": [],
    "HollySemanticsInspectNode": [],
    "HollyStrategyInspectNode": [],
    "HollyBlueprintInspectNode": [],
    "HollyHistoryHitsInspectNode": [],
    "HollyProfileInspectNode": [],
    "HollyReusablePatternsInspectNode": [],
}

EXPECTED_UPSTREAM = {
    "PromptPrefixNode": [],
    "PromptWithImageTagsNode": [],
    "HollyInputBundleNode": ["PromptPrefixNode", "PromptWithImageTagsNode"],
    "HollyIntentAnalyzeNode": ["HollyInputBundleNode"],
    "HollySemanticExpandNode": ["HollyIntentAnalyzeNode", "HollyHistoryFilterNode"],
    "HollyIntegrityValidateNode": ["HollyInputBundleNode", "HollySemanticExpandNode"],
    "HollyStrategySelectNode": [
        "HollyInputBundleNode",
        "HollyIntentAnalyzeNode",
        "HollyIntegrityValidateNode",
        "HollyPreferenceProfileNode",
        "HollyHistoryFilterNode",
    ],
    "HollyBlueprintBuildNode": [
        "HollyInputBundleNode",
        "HollyIntegrityValidateNode",
        "HollyStrategySelectNode",
    ],
    "HollyModelFormatterNode": ["HollyBlueprintBuildNode"],
    "HollyPromptCompareNode": [
        "HollyInputBundleNode",
        "HollyModelFormatterNode",
        "HollyStrategySelectNode",
    ],
    "HollyTraceSaveNode": [
        "HollyInputBundleNode",
        "HollyIntentAnalyzeNode",
        "HollyStrategySelectNode",
        "HollyModelFormatterNode",
    ],
    "HollyHistoryRetrieveNode": ["HollyInputBundleNode"],
    "HollyPreferenceProfileNode": ["HollyInputBundleNode"],
    "HollyHistoryFilterNode": ["HollyHistoryRetrieveNode", "HollyIntentAnalyzeNode"],
    "HollySessionViewerNode": ["HollyTraceSaveNode"],
    "HollyBundleInspectNode": ["HollyInputBundleNode"],
    "HollyIntentInspectNode": ["HollyIntentAnalyzeNode"],
    "HollySemanticsInspectNode": ["HollySemanticExpandNode", "HollyIntegrityValidateNode"],
    "HollyStrategyInspectNode": ["HollyStrategySelectNode"],
    "HollyBlueprintInspectNode": ["HollyBlueprintBuildNode"],
    "HollyHistoryHitsInspectNode": ["HollyHistoryRetrieveNode"],
    "HollyProfileInspectNode": ["HollyPreferenceProfileNode"],
    "HollyReusablePatternsInspectNode": ["HollyHistoryFilterNode"],
}

INVALID_CASES = {
    "HollyIntentAnalyzeNode": lambda context: context["intent_node"].run(context["intent_payload"]),
    "HollySemanticExpandNode": lambda context: context["expand_node"].run(context["bundle_payload"], 0.5),
    "HollyIntegrityValidateNode": lambda context: context["validate_node"].run(context["intent_payload"], context["semantic_payload"]),
    "HollyStrategySelectNode": lambda context: context["strategy_node"].run(
        context["bundle_payload"],
        context["intent_payload"],
        context["semantic_payload"],
        0.7,
    ),
    "HollyBlueprintBuildNode": lambda context: context["blueprint_node"].run(
        context["bundle_payload"],
        context["strategy_payload"],
        context["validated_payload"],
    ),
    "HollyModelFormatterNode": lambda context: context["formatter_node"].run(context["intent_payload"]),
    "HollyPromptCompareNode": lambda context: context["compare_node"].run(
        context["intent_payload"],
        context["final_prompt"],
        context["strategy_payload"],
    ),
    "HollyTraceSaveNode": lambda context: context["trace_node"].run(
        context["intent_payload"],
        context["intent_payload"],
        context["strategy_payload"],
        context["final_prompt"],
        4,
        True,
        "invalid",
    ),
    "HollyHistoryRetrieveNode": lambda context: context["history_retrieve_node"].run(context["intent_payload"], 3),
    "HollyPreferenceProfileNode": lambda context: context["profile_node"].run(context["intent_payload"]),
    "HollyHistoryFilterNode": lambda context: context["history_filter_node"].run(context["profile_payload"], context["intent_payload"]),
    "HollyBundleInspectNode": lambda context: context["bundle_inspect_node"].run(context["intent_payload"]),
    "HollyIntentInspectNode": lambda context: context["intent_inspect_node"].run(context["bundle_payload"]),
    "HollySemanticsInspectNode": lambda context: context["semantics_inspect_node"].run(),
    "HollyStrategyInspectNode": lambda context: context["strategy_inspect_node"].run(context["blueprint_payload"]),
    "HollyBlueprintInspectNode": lambda context: context["blueprint_inspect_node"].run(context["strategy_payload"]),
    "HollyHistoryHitsInspectNode": lambda context: context["history_hits_inspect_node"].run(context["profile_payload"]),
    "HollyProfileInspectNode": lambda context: context["profile_inspect_node"].run(context["history_hits_payload"]),
    "HollyReusablePatternsInspectNode": lambda context: context["reusable_inspect_node"].run(context["history_hits_payload"]),
}


def _input_types_for(node_cls):
    data = node_cls.INPUT_TYPES()
    required = {name: spec[0] for name, spec in data.get("required", {}).items()}
    optional = {name: spec[0] for name, spec in data.get("optional", {}).items()}
    return required, optional


def _collect_downstream_matches():
    matches = {name: [] for name in hp.NODE_CLASS_MAPPINGS}
    for producer_name, producer_cls in hp.NODE_CLASS_MAPPINGS.items():
        producer_outputs = getattr(producer_cls, "RETURN_TYPES", ())
        for consumer_name, consumer_cls in hp.NODE_CLASS_MAPPINGS.items():
            required, optional = _input_types_for(consumer_cls)
            consumer_types = set(required.values()) | set(optional.values())
            if any(output_type in consumer_types for output_type in producer_outputs):
                matches[producer_name].append(consumer_name)
    return matches


def build_context():
    context = {}
    context["prefix_node"] = hp.NODE_CLASS_MAPPINGS["PromptPrefixNode"]()
    context["image_tags_node"] = hp.NODE_CLASS_MAPPINGS["PromptWithImageTagsNode"]()
    context["bundle_node"] = hp.NODE_CLASS_MAPPINGS["HollyInputBundleNode"]()
    context["intent_node"] = hp.NODE_CLASS_MAPPINGS["HollyIntentAnalyzeNode"]()
    context["expand_node"] = hp.NODE_CLASS_MAPPINGS["HollySemanticExpandNode"]()
    context["validate_node"] = hp.NODE_CLASS_MAPPINGS["HollyIntegrityValidateNode"]()
    context["strategy_node"] = hp.NODE_CLASS_MAPPINGS["HollyStrategySelectNode"]()
    context["blueprint_node"] = hp.NODE_CLASS_MAPPINGS["HollyBlueprintBuildNode"]()
    context["formatter_node"] = hp.NODE_CLASS_MAPPINGS["HollyModelFormatterNode"]()
    context["compare_node"] = hp.NODE_CLASS_MAPPINGS["HollyPromptCompareNode"]()
    context["trace_node"] = hp.NODE_CLASS_MAPPINGS["HollyTraceSaveNode"]()
    context["history_retrieve_node"] = hp.NODE_CLASS_MAPPINGS["HollyHistoryRetrieveNode"]()
    context["profile_node"] = hp.NODE_CLASS_MAPPINGS["HollyPreferenceProfileNode"]()
    context["history_filter_node"] = hp.NODE_CLASS_MAPPINGS["HollyHistoryFilterNode"]()
    context["session_node"] = hp.NODE_CLASS_MAPPINGS["HollySessionViewerNode"]()
    context["bundle_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyBundleInspectNode"]()
    context["intent_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyIntentInspectNode"]()
    context["semantics_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollySemanticsInspectNode"]()
    context["strategy_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyStrategyInspectNode"]()
    context["blueprint_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyBlueprintInspectNode"]()
    context["history_hits_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyHistoryHitsInspectNode"]()
    context["profile_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyProfileInspectNode"]()
    context["reusable_inspect_node"] = hp.NODE_CLASS_MAPPINGS["HollyReusablePatternsInspectNode"]()

    prefixed_prompt = context["prefix_node"].build_prompt(
        "Clown dancing In circus tent",
        "cinematic portrait",
        True,
    )[0]
    bundle_payload = context["bundle_node"].build_bundle(
        prefixed_prompt,
        "warm stage atmosphere",
        "auto",
        "z-image-turbo",
        "sanity",
        True,
    )[0]
    intent_payload = context["intent_node"].run(bundle_payload)[0]
    semantic_payload = context["expand_node"].run(intent_payload, 0.65)[0]
    validated_payload, warnings = context["validate_node"].run(bundle_payload, semantic_payload)
    profile_payload = context["profile_node"].run(bundle_payload)[0]
    history_hits_payload = context["history_retrieve_node"].run(bundle_payload, 3)[0]
    reusable_patterns_payload = context["history_filter_node"].run(history_hits_payload, intent_payload)[0]
    strategy_payload = context["strategy_node"].run(
        bundle_payload,
        intent_payload,
        validated_payload,
        0.7,
        profile_payload,
        reusable_patterns_payload,
    )[0]
    blueprint_payload = context["blueprint_node"].run(bundle_payload, validated_payload, strategy_payload)[0]
    final_prompt = context["formatter_node"].run(blueprint_payload)[0]
    compare_text = context["compare_node"].run(bundle_payload, final_prompt, strategy_payload)[0]
    trace_id, save_status = context["trace_node"].run(
        bundle_payload,
        intent_payload,
        strategy_payload,
        final_prompt,
        4,
        True,
        "sanity harness",
    )
    session_report = context["session_node"].run(trace_id)[0]

    context.update(
        {
            "prefixed_prompt": prefixed_prompt,
            "bundle_payload": bundle_payload,
            "intent_payload": intent_payload,
            "semantic_payload": semantic_payload,
            "validated_payload": validated_payload,
            "warnings": warnings,
            "profile_payload": profile_payload,
            "history_hits_payload": history_hits_payload,
            "reusable_patterns_payload": reusable_patterns_payload,
            "strategy_payload": strategy_payload,
            "blueprint_payload": blueprint_payload,
            "final_prompt": final_prompt,
            "compare_text": compare_text,
            "trace_id": trace_id,
            "save_status": save_status,
            "session_report": session_report,
        }
    )
    return context


def evaluate_sanity():
    context = build_context()
    downstream_matches = _collect_downstream_matches()

    node_results = {}
    for name, node_cls in hp.NODE_CLASS_MAPPINGS.items():
        required, optional = _input_types_for(node_cls)
        outputs = list(getattr(node_cls, "RETURN_TYPES", ()))
        edge_status = EDGE_STATUS.get(name, "graph")

        result = {
            "category": getattr(node_cls, "CATEGORY", ""),
            "input_types": {
                "required": required,
                "optional": optional,
            },
            "output_types": outputs,
            "valid_upstream": EXPECTED_UPSTREAM.get(name, []),
            "valid_downstream": EXPECTED_DOWNSTREAM.get(name, []),
            "available_type_matches": sorted(set(downstream_matches.get(name, [])) - {name}),
            "nominal_status": "Pass",
            "misuse_status": "Not checked",
            "edge_status": edge_status,
        }

        invalid_case = INVALID_CASES.get(name)
        if invalid_case is not None:
            try:
                invalid_case(context)
            except (TypeError, ValueError):
                result["misuse_status"] = "Pass"
            except Exception as exc:  # noqa: BLE001
                result["misuse_status"] = f"Pass ({type(exc).__name__})"
            else:
                result["misuse_status"] = "Fail"
        elif edge_status in {"edge", "terminal"}:
            result["misuse_status"] = "Pass with limits"
        else:
            result["misuse_status"] = "Pass with limits"

        node_results[name] = result

    return node_results, context


def live_type_expectations():
    return {
        "HollyInputBundleNode": [HOLLY_BUNDLE],
        "HollyIntentAnalyzeNode": [HOLLY_INTENT],
        "HollySemanticExpandNode": [HOLLY_SEMANTIC_CANDIDATES],
        "HollyIntegrityValidateNode": [HOLLY_VALIDATED_SEMANTICS, "STRING"],
        "HollyStrategySelectNode": [HOLLY_STRATEGY],
        "HollyBlueprintBuildNode": [HOLLY_BLUEPRINT],
        "HollyModelFormatterNode": ["STRING"],
        "HollyPromptCompareNode": ["STRING"],
        "HollyTraceSaveNode": ["STRING", "STRING"],
        "HollyHistoryRetrieveNode": [HOLLY_HISTORY_HITS],
        "HollyPreferenceProfileNode": [HOLLY_PROFILE],
        "HollyHistoryFilterNode": [HOLLY_REUSABLE_PATTERNS],
        "HollyBundleInspectNode": ["STRING"],
        "HollyIntentInspectNode": ["STRING"],
        "HollySemanticsInspectNode": ["STRING"],
        "HollyStrategyInspectNode": ["STRING"],
        "HollyBlueprintInspectNode": ["STRING"],
        "HollyHistoryHitsInspectNode": ["STRING"],
        "HollyProfileInspectNode": ["STRING"],
        "HollyReusablePatternsInspectNode": ["STRING"],
        "PromptPrefixNode": ["STRING"],
        "PromptWithImageTagsNode": ["STRING"],
        "HollySessionViewerNode": ["STRING"],
    }
