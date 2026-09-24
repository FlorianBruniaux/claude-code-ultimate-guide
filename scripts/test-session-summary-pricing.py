#!/usr/bin/env python3
"""Exercise the fallback pricing function without running SessionEnd side effects."""
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = Path(sys.argv.pop(1)) if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else ROOT / 'examples/hooks/bash/session-summary.sh'
SOURCE = HOOK.read_text()
FUNCTION = re.search(r'^get_pricing\(\) \{\n.*?^\}', SOURCE, re.M | re.S).group(0)

class PricingTest(unittest.TestCase):
    def test_standard_rates(self):
        cases = {
            'claude-opus-5-5': ('4.00', '20.00'),
            'claude-opus-5': ('5.00', '25.00'),
            'claude-opus-4-8': ('5.00', '25.00'),
            'claude-opus-4-6': ('5.00', '25.00'),
            'claude-sonnet-5': ('2.00', '10.00'),
            'claude-sonnet-4-6': ('3.00', '15.00'),
            'claude-haiku-4-5': ('1.00', '5.00'),
            'claude-haiku-4-5-20251001': ('1.00', '5.00'),
            'claude-fable-5-1': ('10.00', '50.00'),
            'claude-fable-5': ('10.00', '50.00'),
        }
        for model, expected in cases.items():
            with self.subTest(model=model):
                result = subprocess.run(['bash', '-c', FUNCTION + '\nget_pricing "$1" input\nget_pricing "$1" output', 'pricing-test', model], text=True, capture_output=True, check=True)
                self.assertEqual(tuple(result.stdout.splitlines()), expected)

if __name__ == '__main__':
    unittest.main()
