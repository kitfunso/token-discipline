from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class SkillPolicyTests(unittest.TestCase):
    def _skill_description(self) -> str:
        lines = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()

        for line in lines:
            if line.startswith("description:"):
                return line.partition(":")[2].strip()

        self.fail("SKILL.md is missing a description field in the frontmatter")

    def test_skill_contains_low_budget_guardrails_for_recent_regressions(self):
        text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("do not use memory_search", text)
        self.assertIn("assume the current repo", text)
        self.assertIn("do not spend a low-budget tool call rereading this skill", text)

    def test_skill_description_covers_recent_openclaw_trigger_misses(self):
        description = self._skill_description()

        self.assertIn("old version", description)
        self.assertIn("stale badge", description)
        self.assertIn("release tag", description)
        self.assertIn("current repo", description)
        self.assertIn("ready to push", description)


if __name__ == "__main__":
    unittest.main()
