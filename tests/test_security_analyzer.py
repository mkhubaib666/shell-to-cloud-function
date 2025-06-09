import unittest
from src.security import SecurityAnalyzer


class TestSecurityAnalyzer(unittest.TestCase):
    def test_safe_script(self):
        analyzer = SecurityAnalyzer({"interactive_prompt": False})
        script = 'echo "hello"\nls -l'
        self.assertTrue(analyzer.scan(script))

    def test_dangerous_rm_script(self):
        analyzer = SecurityAnalyzer({"interactive_prompt": False})
        script = "rm -rf /"
        # In non-interactive mode, it should fail the check
        self.assertFalse(analyzer.scan(script))

    def test_dangerous_dd_script(self):
        analyzer = SecurityAnalyzer({"interactive_prompt": False})
        script = "dd if=/dev/zero of=/dev/sda"
        self.assertFalse(analyzer.scan(script))