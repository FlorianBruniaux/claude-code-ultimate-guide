#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from clean_trivial_prose import transform_markdown


SCRIPT = Path(__file__).with_name("clean_trivial_prose.py")


class TransformMarkdownTests(unittest.TestCase):
    def test_rewrites_only_structural_em_dash_separators(self):
        source = """# Claude Code — For Tech Leads

| Concern | WP05 — Deploying with a Team |

- **Config audit** — review the current setup
- [Full Guide](../guide.md) — start with team configuration
- [Guide Ch.3.5 — Team Configuration](../guide.md#team)
- Whitepapers — 10 focused guides

The gap isn't adoption — it's structured adoption.
"""
        expected = """# Claude Code: For Tech Leads

| Concern | WP05: Deploying with a Team |

- **Config audit**: review the current setup
- [Full Guide](../guide.md): start with team configuration
- [Guide Ch.3.5: Team Configuration](../guide.md#team)
- Whitepapers: 10 focused guides

The gap isn't adoption — it's structured adoption.
"""

        result = transform_markdown(source)

        self.assertEqual(expected, result.text)
        self.assertEqual(6, result.replacements)
        self.assertEqual([(10, "The gap isn't adoption — it's structured adoption.")], result.remaining)

    def test_preserves_blockquotes_fenced_code_and_inline_code(self):
        source = """> Literal quotation — preserve it.

```markdown
# Example — Preserve
- **Label** — preserve
```

- Run `printf 'a — b'` — then inspect the output
"""

        result = transform_markdown(source)

        self.assertEqual(source, result.text)
        self.assertEqual(0, result.replacements)
        self.assertEqual(
            [
                (1, "> Literal quotation — preserve it."),
                (8, "- Run `printf 'a — b'` — then inspect the output"),
            ],
            result.remaining,
        )

    def test_rewrites_known_rhetorical_heading_but_preserves_unknown_subheadings(self):
        source = """### The learning curve is real — here's how to manage it

### The learning curve is real: here's how to manage it

### A claim — needs editorial judgment

| License budget | ✅ | — | — |
"""
        expected = """### Managing the learning curve

### Managing the learning curve

### A claim — needs editorial judgment

| License budget | ✅ | — | — |
"""

        result = transform_markdown(source)

        self.assertEqual(expected, result.text)
        self.assertEqual(2, result.replacements)
        self.assertEqual(
            [(5, "### A claim — needs editorial judgment")],
            result.remaining,
        )

    def test_removes_one_trailing_space_from_a_changed_line(self):
        source = "# Claude Code — For Managers \n"

        result = transform_markdown(source)

        self.assertEqual("# Claude Code: For Managers\n", result.text)
        self.assertEqual(1, result.replacements)

    def test_preserves_em_dash_inside_a_quoted_title(self):
        source = '# Resource Evaluation: "Comprehension Debt — The Hidden Cost"\n'

        result = transform_markdown(source)

        self.assertEqual(source, result.text)
        self.assertEqual(0, result.replacements)
        self.assertEqual(
            [(1, '# Resource Evaluation: "Comprehension Debt — The Hidden Cost"')],
            result.remaining,
        )

    def test_preserves_em_dash_inside_an_inline_quotation(self):
        source = '**Line 238**: Added "[SE-CoVe](./se-cove.md) — Chain-of-Verification"\n'

        result = transform_markdown(source)

        self.assertEqual(source, result.text)
        self.assertEqual(0, result.replacements)
        self.assertEqual(
            [
                (
                    1,
                    '**Line 238**: Added "[SE-CoVe](./se-cove.md) — Chain-of-Verification"',
                )
            ],
            result.remaining,
        )


class CommandLineTests(unittest.TestCase):
    def test_check_fails_before_write_and_passes_after_write(self):
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "page.md"
            document.write_text(
                "# Claude Code — For Managers\n\nA claim — needs judgment.\n",
                encoding="utf-8",
            )

            before = subprocess.run(
                [sys.executable, str(SCRIPT), "--check", "--verbose", str(document)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, before.returncode)
            self.assertIn("1 safe replacement available", before.stdout)
            self.assertIn("1 ambiguous line remains", before.stdout)
            self.assertIn(
                f"{document}:1: # Claude Code — For Managers => # Claude Code: For Managers",
                before.stdout,
            )

            write = subprocess.run(
                [sys.executable, str(SCRIPT), "--write", str(document)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, write.returncode)
            self.assertEqual(
                "# Claude Code: For Managers\n\nA claim — needs judgment.\n",
                document.read_text(encoding="utf-8"),
            )

            after = subprocess.run(
                [sys.executable, str(SCRIPT), "--check", str(document)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, after.returncode)
            self.assertIn("0 safe replacements available", after.stdout)
            self.assertIn("1 ambiguous line remains", after.stdout)


if __name__ == "__main__":
    unittest.main()
