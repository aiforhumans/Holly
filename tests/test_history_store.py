import os
import tempfile
import unittest

from services.history_store import get_profile, retrieve_similar, save_trace


class HistoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = os.environ.get("HOLLY_PROMPT_DB_PATH")
        os.environ["HOLLY_PROMPT_DB_PATH"] = os.path.join(self.temp_dir.name, "test_holly_prompt.db")

    def tearDown(self):
        if self.old_db_path is None:
            os.environ.pop("HOLLY_PROMPT_DB_PATH", None)
        else:
            os.environ["HOLLY_PROMPT_DB_PATH"] = self.old_db_path
        self.temp_dir.cleanup()

    def test_retrieve_similar_can_scope_by_user(self):
        save_trace(
            {
                "user_id": "alice",
                "raw_prompt": "clown dancing in circus tent",
                "final_prompt": "playful clown dancing in a warm circus tent",
                "target_model": "z-image-turbo",
                "intent_map": {"subject": "clown"},
                "strategy_profile": {"mode": "enhance"},
                "score": 5,
                "liked": True,
                "notes": "",
            }
        )
        save_trace(
            {
                "user_id": "bob",
                "raw_prompt": "castle at sunrise",
                "final_prompt": "stone castle at sunrise over mountains",
                "target_model": "z-image-turbo",
                "intent_map": {"subject": "castle"},
                "strategy_profile": {"mode": "enhance"},
                "score": 4,
                "liked": True,
                "notes": "",
            }
        )

        alice_hits = retrieve_similar("clown in circus", top_k=5, user_id="alice")
        bob_hits = retrieve_similar("clown in circus", top_k=5, user_id="bob")

        self.assertTrue(alice_hits)
        self.assertEqual(len(bob_hits), 1)
        self.assertIn("castle", bob_hits[0]["raw_prompt"])
        self.assertTrue(all("clown" in h["raw_prompt"] or "clown" in h["final_prompt"] for h in alice_hits))

    def test_get_profile_updates_after_save(self):
        save_trace(
            {
                "user_id": "carol",
                "raw_prompt": "robot portrait",
                "final_prompt": "robot portrait with clean studio lighting",
                "target_model": "z-image-turbo",
                "intent_map": {"subject": "robot"},
                "strategy_profile": {"mode": "preserve"},
                "score": 3,
                "liked": False,
                "notes": "",
            }
        )
        profile = get_profile("carol")
        self.assertEqual(profile["user_id"], "carol")
        self.assertGreaterEqual(profile["prompt_count"], 1)


if __name__ == "__main__":
    unittest.main()
