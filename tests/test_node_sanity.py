import os
import tempfile
import unittest

from sanity_harness import EDGE_STATUS, evaluate_sanity


class NodeSanityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = os.environ.get("HOLLY_PROMPT_DB_PATH")
        os.environ["HOLLY_PROMPT_DB_PATH"] = os.path.join(self.temp_dir.name, "node_sanity.db")

    def tearDown(self):
        if self.old_db_path is None:
            os.environ.pop("HOLLY_PROMPT_DB_PATH", None)
        else:
            os.environ["HOLLY_PROMPT_DB_PATH"] = self.old_db_path
        self.temp_dir.cleanup()

    def test_all_nodes_have_nominal_behavior_and_counterparts(self):
        results, _context = evaluate_sanity()

        for name, result in results.items():
            self.assertEqual(result["nominal_status"], "Pass", name)

            edge_status = EDGE_STATUS.get(name, "graph")
            if edge_status == "graph":
                self.assertTrue(result["valid_downstream"], f"{name} missing valid downstream counterpart")
                self.assertTrue(result["valid_upstream"], f"{name} missing valid upstream counterpart")

    def test_typed_nodes_reject_wrong_contracts(self):
        results, _context = evaluate_sanity()
        for name, result in results.items():
            if EDGE_STATUS.get(name, "graph") == "graph":
                self.assertNotEqual(result["misuse_status"], "Fail", name)


if __name__ == "__main__":
    unittest.main()

