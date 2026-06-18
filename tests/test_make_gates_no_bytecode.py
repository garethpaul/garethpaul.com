import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHILD_MARKER = "GARETHPAUL_BYTECODE_GATE_CHILD"


class MakeGateNoBytecodeTest(unittest.TestCase):
    def test_make_check_does_not_write_repository_bytecode(self):
        if os.environ.get(CHILD_MARKER) == "1":
            self.skipTest("nested gate invocation")

        with tempfile.TemporaryDirectory() as temporary_directory:
            copied_root = Path(temporary_directory) / "repository"
            shutil.copytree(
                ROOT,
                copied_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo"),
            )
            subprocess.run(["git", "init", "-q"], cwd=str(copied_root), check=True)
            subprocess.run(["git", "add", "-A"], cwd=str(copied_root), check=True)

            env = os.environ.copy()
            env.pop("PYTHONDONTWRITEBYTECODE", None)
            env.pop("PYTHONPYCACHEPREFIX", None)
            env[CHILD_MARKER] = "1"
            result = subprocess.run(
                ["make", "check"],
                cwd=str(copied_root),
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            bytecode_paths = sorted(
                path.relative_to(copied_root)
                for path in copied_root.rglob("*")
                if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo"}
            )
            self.assertEqual([], bytecode_paths)


if __name__ == "__main__":
    unittest.main()
