import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "aliasrecordreview"


class CliTests(unittest.TestCase):
    def run_cli(self, path):
        return subprocess.run(
            [sys.executable, "-m", PACKAGE, str(path)],
            capture_output=True,
            text=True,
            timeout=12,
        )

    def test_good_and_input_preserved(self):
        path = ROOT / "examples/valid.bin"
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        r = self.run_cli(path)
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        doc = json.loads(r.stdout)
        self.assertEqual(doc["input_sha256"], before)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

    def test_invalid_input(self):
        r = self.run_cli(ROOT / "examples/invalid.bin")
        self.assertEqual(r.returncode, 1, r.stderr + r.stdout)
        self.assertEqual(json.loads(r.stdout)["status"], "FAIL")
        self.assertNotIn("Traceback", r.stderr)

    def test_read_error_private(self):
        r = self.run_cli(ROOT / "examples/nonexistent_private_path")
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("nonexistent_private_path", r.stdout + r.stderr)

    def test_no_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            link = Path(d) / "alias"
            link.symlink_to(ROOT / "examples/valid.bin")
            r = self.run_cli(link)
            self.assertEqual(r.returncode, 1)

    def test_unsupported_input(self):
        r = self.run_cli(ROOT / "examples/unsupported.bin")
        self.assertEqual(r.returncode, 2, r.stderr + r.stdout)
        self.assertEqual(json.loads(r.stdout)["status"], "OPEN")
