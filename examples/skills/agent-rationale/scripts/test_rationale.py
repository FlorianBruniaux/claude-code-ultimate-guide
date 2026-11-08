"""Behavior tests for rationale.py, run in throwaway Git repositories.

Run from the repository root:
    python3 -I examples/skills/agent-rationale/scripts/test_rationale.py
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rationale.py")
NOTES_REF = "refs/notes/rationale"


class Repo:
    def __init__(self, root):
        self.root = root
        self.env = dict(os.environ)
        self.env.update({
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "tester",
            "GIT_AUTHOR_EMAIL": "tester@example.invalid",
            "GIT_COMMITTER_NAME": "tester",
            "GIT_COMMITTER_EMAIL": "tester@example.invalid",
        })

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, env=self.env,
                              capture_output=True, text=True, check=True).stdout

    def write(self, name, text):
        with open(os.path.join(self.root, name), "w") as handle:
            handle.write(text)

    def commit(self, message, *, amend=False):
        self.git("add", "-A")
        if amend:
            self.git("commit", "-q", "--amend", "--no-edit")
        else:
            self.git("commit", "-q", "-m", message)

    def rationale(self, *args, check=True):
        result = subprocess.run([sys.executable, "-I", SCRIPT, *args], cwd=self.root,
                                env=self.env, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise AssertionError(f"rationale.py {args} failed: {result.stderr}")
        return result


BASE = "def total(items):\n    return sum(items)\n"
CHANGE = (
    "def total(items):\n"
    "    if not items:\n"
    "        return 0\n"
    "    return sum(item.price for item in items)\n"
)

NOTE_ARGS = [
    "add", "--file", "cart.py", "--line", "4",
    "--intent", "Sum prices, not item objects",
    "--rejected", "Keep sum(items) and give Item an __add__ method",
    "--risk", "Items without a price attribute now raise AttributeError",
    "--evidence", "test_cart.py::test_total_uses_price",
    "--open-question", "unknown",
]


class RationaleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Repo(self.tmp.name)
        self.repo.git("init", "-q", "-b", "main")
        self.repo.write("cart.py", BASE)
        self.repo.commit("base")
        self.repo.git("checkout", "-q", "-b", "feature")
        self.repo.write("cart.py", CHANGE)
        self.repo.commit("agent change")

    def tearDown(self):
        self.tmp.cleanup()

    def note(self):
        return json.loads(self.repo.git("notes", f"--ref={NOTES_REF}", "show", "HEAD"))

    def show(self):
        return json.loads(self.repo.rationale("show", "--json").stdout)

    def test_add_writes_a_note_with_all_fields(self):
        self.repo.rationale(*NOTE_ARGS)
        note = self.note()
        self.assertEqual(note["schema"], "agent-rationale/1")
        [entry] = note["notes"]
        self.assertEqual(entry["file"], "cart.py")
        self.assertEqual(entry["intent"], "Sum prices, not item objects")
        self.assertEqual(entry["rejected_alternative"], "Keep sum(items) and give Item an __add__ method")
        self.assertEqual(entry["risk"], "Items without a price attribute now raise AttributeError")
        self.assertEqual(entry["evidence"], "test_cart.py::test_total_uses_price")
        self.assertEqual(entry["open_question"], "unknown")
        self.assertEqual(entry["snippet"], "    return sum(item.price for item in items)")
        self.assertTrue(entry["hunk_hash"].startswith("sha256:"))

    def test_line_outside_the_commit_diff_is_refused(self):
        result = self.repo.rationale("add", "--file", "cart.py", "--line", "1",
                                     "--intent", "x", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not in a hunk", result.stderr)

    def test_missing_intent_is_refused(self):
        result = self.repo.rationale("add", "--file", "cart.py", "--line", "4", check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_unchanged_hunk_is_anchored(self):
        self.repo.rationale(*NOTE_ARGS)
        [entry] = self.show()
        self.assertEqual(entry["status"], "anchored")
        self.assertEqual(entry["line"], 4)

    def test_note_follows_amend_and_rebase_with_rewrite_ref(self):
        self.repo.git("config", "notes.rewriteRef", NOTES_REF)
        self.repo.rationale(*NOTE_ARGS)
        self.repo.write("README.md", "cart\n")
        self.repo.commit("", amend=True)
        self.assertEqual(self.note()["notes"][0]["intent"], "Sum prices, not item objects")
        self.repo.git("checkout", "-q", "main")
        self.repo.write("other.py", "x = 1\n")
        self.repo.commit("other")
        self.repo.git("checkout", "-q", "feature")
        self.repo.git("rebase", "-q", "main")
        self.assertEqual(self.note()["notes"][0]["intent"], "Sum prices, not item objects")
        self.assertEqual(self.show()[0]["status"], "anchored")

    def test_line_shift_keeps_the_note_on_its_line(self):
        self.repo.git("config", "notes.rewriteRef", NOTES_REF)
        self.repo.rationale(*NOTE_ARGS)
        self.repo.write("cart.py", "# cart helpers\n\n" + CHANGE)
        self.repo.commit("", amend=True)
        [entry] = self.show()
        self.assertEqual(entry["status"], "anchored")
        self.assertEqual(entry["line"], 6)

    def test_edit_elsewhere_in_the_hunk_reanchors_by_snippet(self):
        self.repo.git("config", "notes.rewriteRef", NOTES_REF)
        self.repo.rationale(*NOTE_ARGS)
        self.repo.write("cart.py", CHANGE.replace("return 0", "return 0.0"))
        self.repo.commit("", amend=True)
        [entry] = self.show()
        self.assertEqual(entry["status"], "reanchored")
        self.assertEqual(entry["line"], 4)

    def test_edit_of_the_annotated_line_marks_the_note_stale(self):
        self.repo.git("config", "notes.rewriteRef", NOTES_REF)
        self.repo.rationale(*NOTE_ARGS)
        self.repo.write("cart.py", CHANGE.replace("item.price", "item.unit_price"))
        self.repo.commit("", amend=True)
        [entry] = self.show()
        self.assertEqual(entry["status"], "stale")
        self.assertIsNone(entry["line"])

    def test_without_rewrite_ref_amend_leaves_no_note(self):
        self.repo.rationale(*NOTE_ARGS)
        self.repo.write("README.md", "cart\n")
        self.repo.commit("", amend=True)
        result = subprocess.run(["git", "notes", f"--ref={NOTES_REF}", "show", "HEAD"],
                                cwd=self.repo.root, env=self.repo.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)


    def test_added_line_starting_with_plus_plus_is_kept(self):
        self.repo.write("count.c", "int n;\n++n;\nreturn n;\n")
        self.repo.commit("counter")
        self.repo.rationale("add", "--file", "count.c", "--line", "3", "--intent", "Return the count")
        [entry] = self.show()
        self.assertEqual(entry["snippet"], "return n;")
        self.assertEqual((entry["status"], entry["line"]), ("anchored", 3))

    def test_form_feed_inside_a_line_keeps_the_whole_line(self):
        self.repo.write("page.txt", "first\fsame line\nsecond\n")
        self.repo.commit("page")
        self.repo.rationale("add", "--file", "page.txt", "--line", "1", "--intent", "First line")
        self.repo.rationale("add", "--file", "page.txt", "--line", "2", "--intent", "Second line")
        notes = self.note()["notes"]
        self.assertEqual(notes[0]["snippet"], "first\fsame line")
        self.assertEqual(notes[1]["snippet"], "second")

    def test_duplicate_line_in_a_hunk_anchors_to_the_annotated_occurrence(self):
        self.repo.write("dup.py", "a = 1\npass\nb = 2\npass\n")
        self.repo.commit("dup")
        self.repo.rationale("add", "--file", "dup.py", "--line", "4", "--intent", "Second pass")
        [entry] = self.show()
        self.assertEqual((entry["status"], entry["line"]), ("anchored", 4))

    def test_ambiguous_snippet_after_an_edit_is_stale_not_guessed(self):
        self.repo.git("config", "notes.rewriteRef", NOTES_REF)
        self.repo.write("dup.py", "a = 1\npass\nb = 2\npass\n")
        self.repo.commit("dup")
        self.repo.rationale("add", "--file", "dup.py", "--line", "4", "--intent", "Second pass")
        self.repo.write("dup.py", "a = 10\npass\nb = 2\npass\n")
        self.repo.commit("", amend=True)
        [entry] = self.show()
        self.assertEqual(entry["status"], "stale")

    def test_non_json_note_is_reported_not_a_traceback(self):
        self.repo.git("notes", f"--ref={NOTES_REF}", "add", "-m", "written by a person", "HEAD")
        result = self.repo.rationale("show", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not an agent-rationale note", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_paths_are_stored_from_the_repository_root(self):
        os.makedirs(os.path.join(self.repo.root, "src"))
        self.repo.write("src/m.py", "x = 1\n")
        self.repo.commit("m")
        subprocess.run([sys.executable, "-I", SCRIPT, "add", "--file", "m.py", "--line", "1", "--intent", "x"],
                       cwd=os.path.join(self.repo.root, "src"), env=self.repo.env, check=True, capture_output=True)
        self.assertEqual(self.note()["notes"][0]["file"], "src/m.py")
        self.assertEqual(self.show()[0]["status"], "anchored")


if __name__ == "__main__":
    unittest.main(verbosity=2)
