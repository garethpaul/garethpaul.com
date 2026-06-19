import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BaselineNoBytecodeTest(unittest.TestCase):
    def test_checker_does_not_write_redirected_bytecode(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_root = Path(temporary_directory) / "pycache"
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONPYCACHEPREFIX"] = str(cache_root)

            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/check-baseline.py")],
                cwd=str(ROOT),
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            cache_files = [path for path in cache_root.rglob("*") if path.is_file()]
            self.assertEqual([], cache_files)


if __name__ == "__main__":
    unittest.main()
