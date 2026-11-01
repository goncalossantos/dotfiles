"""Optional real chezmoi integration test in a disposable HOME."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
CHEZMOI = os.environ.get("CHEZMOI_BIN") or shutil.which("chezmoi")


@unittest.skipUnless(CHEZMOI, "Set CHEZMOI_BIN or install chezmoi to run the integration test")
class ChezmoiTests(unittest.TestCase):
    def test_diff_dry_run_apply_and_idempotence(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-chezmoi-test-") as temp:
            base = Path(temp)
            home = base / "isolated home"
            home.mkdir()
            config = base / "chezmoi.toml"
            config.write_text("[data]\ndotfilesRoot = " + json.dumps(str(REPO)) + "\n")
            env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(base / "config"),
                       XDG_DATA_HOME=str(base / "data"), XDG_CACHE_HOME=str(base / "cache"),
                       XDG_STATE_HOME=str(base / "state"))
            command = [CHEZMOI, "--config", str(config), "--source", str(REPO / "agentic/chezmoi"),
                       "--destination", str(home), "--no-pager"]

            def run(*args):
                result = subprocess.run([*command, *args], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result.stdout

            # Unmanaged content must survive; only the seven declared paths are managed.
            unrelated = home / "keep-me.txt"
            unrelated.write_text("not managed\n")
            self.assertIn("visual-explainer", run("diff"))
            run("apply", "--dry-run")
            self.assertEqual(list(home.iterdir()), [unrelated])
            run("apply")
            links = [p for p in home.rglob("*") if p.is_symlink()]
            self.assertEqual(len(links), 7)
            self.assertTrue(all(p.exists() for p in links))
            self.assertEqual((home / ".claude/CLAUDE.md").resolve(),
                             REPO / "agentic/instructions/AGENTS.md")
            self.assertTrue((home / ".agents/skills/i-have-adhd/LICENSE").is_file())
            self.assertEqual(run("diff"), "")
            run("apply")
            run("verify")
            self.assertEqual(unrelated.read_text(), "not managed\n")
            # Introduce drift in a managed symlink. A diff should expose it.
            link = home / ".codex/AGENTS.md"
            link.unlink()
            link.symlink_to(unrelated)
            self.assertNotEqual(run("diff"), "")
            # Drift normally prompts for approval; this test has no TTY. Force is
            # paired with dry-run here only, so no managed file is overwritten.
            run("apply", "--dry-run", "--force")
            self.assertEqual(link.resolve(), unrelated)


if __name__ == "__main__":
    unittest.main()
