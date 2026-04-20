import pathlib
import sys
import unittest


class RegistrationTests(unittest.TestCase):
    def test_node_mappings_contain_expected_nodes(self):
        package_root = pathlib.Path(__file__).resolve().parents[1]
        custom_nodes_root = package_root.parent
        sys.path.insert(0, str(custom_nodes_root))
        try:
            import Holly_prompt as hp
        finally:
            try:
                sys.path.remove(str(custom_nodes_root))
            except ValueError:
                pass

        required = {
            "PromptPrefixNode",
            "PromptWithImageTagsNode",
            "HollyInputBundleNode",
            "HollyIntentAnalyzeNode",
            "HollySemanticExpandNode",
            "HollyIntegrityValidateNode",
            "HollyStrategySelectNode",
            "HollyBlueprintBuildNode",
            "HollyModelFormatterNode",
            "HollyPromptCompareNode",
            "HollyTraceSaveNode",
            "HollyHistoryRetrieveNode",
            "HollyPreferenceProfileNode",
            "HollyHistoryFilterNode",
            "HollySessionViewerNode",
            "HollyBundleInspectNode",
            "HollyIntentInspectNode",
            "HollySemanticsInspectNode",
            "HollyStrategyInspectNode",
            "HollyBlueprintInspectNode",
            "HollyHistoryHitsInspectNode",
            "HollyProfileInspectNode",
            "HollyReusablePatternsInspectNode",
        }
        self.assertTrue(required.issubset(set(hp.NODE_CLASS_MAPPINGS.keys())))


if __name__ == "__main__":
    unittest.main()
