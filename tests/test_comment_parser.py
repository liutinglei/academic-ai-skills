import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "reviewer-response"
    / "scripts"
    / "comment_parser.py"
)

spec = importlib.util.spec_from_file_location("comment_parser", SCRIPT_PATH)
comment_parser = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["comment_parser"] = comment_parser
spec.loader.exec_module(comment_parser)


class CommentParserTests(unittest.TestCase):
    def test_parses_reviewer_headings_and_numbered_comments(self):
        text = """Reviewer 1:
1. Clarify the research gap.
2. Add participant details.

Reviewer 2:
- Improve Table 2 labels.
"""
        comments = comment_parser.parse_comments(text)

        self.assertEqual([comment.id for comment in comments], [
            "Reviewer 1, Comment 1",
            "Reviewer 1, Comment 2",
            "Reviewer 2, Comment 1",
        ])
        self.assertIn("research gap", comments[0].text)
        self.assertIn("participant", comments[1].text)
        self.assertIn("Table 2", comments[2].text)
        self.assertFalse(comments[2].text.startswith("-"))

    def test_preserves_multiline_comment_text(self):
        text = """Editor:
Please revise the cover letter.
Include a concise summary of major changes.
"""
        comments = comment_parser.parse_comments(text)

        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].source, "Editor")
        self.assertIn("concise summary", comments[0].text)

    def test_accepts_hash_in_reviewer_heading(self):
        text = """Reviewer #1:
Comment 1: Clarify the sampling frame.
"""
        comments = comment_parser.parse_comments(text)

        self.assertEqual(comments[0].id, "Reviewer #1, Comment 1")
        self.assertIn("sampling frame", comments[0].text)

    def test_cli_outputs_json(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--json",
            ],
            input="Reviewer 1:\n1. Clarify the research gap.\n",
            text=True,
            capture_output=True,
            check=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload[0]["id"], "Reviewer 1, Comment 1")
        self.assertEqual(payload[0]["source"], "Reviewer 1")


if __name__ == "__main__":
    unittest.main()
