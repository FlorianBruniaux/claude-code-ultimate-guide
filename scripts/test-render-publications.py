#!/usr/bin/env python3
"""Behavior checks for the bilingual export inventory and preprocessing."""
import importlib.util
import unittest
from collections import Counter
from pathlib import Path


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


render = load("render-publications")
preprocess = load("preprocess-guide")


class PublicationBuildTests(unittest.TestCase):
    def test_complete_public_catalog(self):
        jobs = render.inventory(render.ROOT, ("en", "fr"), render.COLLECTIONS, ("pdf", "epub"))
        self.assertEqual(len(jobs), 174)
        self.assertEqual(len({job["output"] for job in jobs}), 174)
        counts = Counter((job["language"], Path(job["output"]).suffix) for job in jobs)
        self.assertEqual(counts, {("en", ".pdf"): 73, ("fr", ".pdf"): 73,
                                  ("en", ".epub"): 14, ("fr", ".epub"): 14})

    def test_french_guide_uses_french_wrapper(self):
        jobs = render.inventory(render.ROOT, ("fr",), ("guides",), ("pdf",))
        self.assertEqual(jobs[0]["source"], "whitepapers/guide-export-fr.qmd")
        self.assertEqual(jobs[0]["output"], "guides/fr/guide-export-fr.pdf")

    def test_manual_toc_removed_in_both_languages(self):
        for title, note in (("Table of Contents", "See the Table"),
                            ("Table des matières", "Consultez la table")):
            content = f"Intro\n\n## {title}\n\n- duplicated index\n\n## 1.1 Installation\n\nBody\n"
            result = preprocess.strip_inline_toc(content)
            self.assertNotIn("duplicated index", result)
            self.assertIn(note, result)
            self.assertTrue(result.startswith("Intro\n\n"))
            self.assertTrue(result.endswith("## 1.1 Installation\n\nBody\n"))

    def test_unrecognized_toc_boundary_preserves_content(self):
        content = "## Table des matières\n\nContent with no installation section\n"
        self.assertEqual(preprocess.strip_inline_toc(content), content)

    def test_nested_code_fences_preserve_examples(self):
        content = "````markdown\nExample:\n```bash\n@agent command\n```\nList:\n- example\n````\nText:\n- actual list\n@agent\n"
        result = preprocess.ensure_blank_before_lists(preprocess.escape_citation_patterns(content))
        self.assertIn("```bash\n@agent command\n```\nList:\n- example", result)
        self.assertIn("Text:\n\n- actual list\n\\@agent", result)


if __name__ == "__main__":
    unittest.main()
