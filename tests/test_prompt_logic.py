import json
import unittest

from core.prompt_logic import analyze_intent, parse_json_or_text


class PromptLogicTests(unittest.TestCase):
    def test_parse_json_or_text_accepts_json_list(self):
        payload = json.dumps([{"trace_id": "1"}, {"trace_id": "2"}])
        parsed = parse_json_or_text(payload)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 2)

    def test_analyze_intent_handles_mixed_case_in(self):
        intent = analyze_intent({"user_prompt": "Clown dancing In circus tent"})
        self.assertIn("clown", intent["subject"].lower())
        self.assertIn("circus tent", intent["setting"].lower())
        self.assertEqual(intent["action"], "dancing")


if __name__ == "__main__":
    unittest.main()
