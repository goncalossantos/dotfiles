"""Filesystem-only tests; no agents, authentication, or paid requests are started."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "agentic/scripts/setup.py"
spec = importlib.util.spec_from_file_location("setup", SCRIPT)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dotfiles-test-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home with spaces"
        self.home.mkdir()
        self.env = {k: v for k, v in os.environ.items()
                    if k not in ("PI_CODING_AGENT_DIR", "CLAUDE_CONFIG_DIR", "CODEX_HOME")}

    def run_setup(self, *args, ok=True, env=None):
        result = subprocess.run([sys.executable, str(SCRIPT), "--home", str(self.home), *args],
                                env=env or self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_dry_run_changes_nothing(self):
        self.run_setup()
        self.assertEqual(list(self.home.iterdir()), [])

    def test_apply_idempotent_and_remove(self):
        self.run_setup("--apply")
        plan = setup.make_plan(self.home, setup.CLIENTS)
        self.assertEqual(len(plan), 7)
        for target, source in plan.items():
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), source.resolve())
        # Entire directories are linked: license and real-path relative references survive.
        visual = self.home / ".agents/skills/visual-explainer"
        self.assertTrue((visual.resolve() / "../../research/explainer-video-services.md").is_file())
        self.assertTrue((self.home / ".agents/skills/i-have-adhd/LICENSE").is_file())
        self.run_setup("--apply")
        self.run_setup("--remove")
        self.assertTrue(all(t.is_symlink() for t in plan))
        self.run_setup("--remove", "--apply")
        self.assertTrue(all(not os.path.lexists(t) for t in plan))
        self.run_setup("--remove", "--apply")

    def test_conflict_preflight_does_not_write_any_links(self):
        target = self.home / ".codex/AGENTS.md"
        target.parent.mkdir()
        target.write_text("Existing preferences\n")
        self.run_setup("--apply", ok=False)
        self.assertEqual(target.read_text(), "Existing preferences\n")
        self.assertFalse((self.home / ".pi").exists())

    def test_foreign_and_dangling_links_are_not_replaced_or_removed(self):
        target = self.home / ".claude/CLAUDE.md"
        target.parent.mkdir()
        target.symlink_to(self.home / "missing.md")
        self.run_setup("--client", "claude", "--apply", ok=False)
        self.run_setup("--client", "claude", "--remove", "--apply", ok=False)
        self.assertTrue(target.is_symlink())

    def test_single_client_and_custom_directory(self):
        custom = self.home / "custom pi"
        self.run_setup("--client", "pi", "--pi-dir", str(custom), "--apply")
        self.assertTrue((custom / "AGENTS.md").is_symlink())
        self.assertTrue((self.home / ".agents/skills/visual-explainer").is_dir())
        self.assertFalse((self.home / ".claude").exists())
        self.assertFalse((self.home / ".codex").exists())

    def test_environment_override_requires_explicit_acknowledgement(self):
        env = dict(self.env, CODEX_HOME=str(self.home / "other-codex"))
        self.run_setup("--client", "codex", "--apply", env=env, ok=False)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_higher_priority_override_requires_review(self):
        override = self.home / ".codex/AGENTS.override.md"
        override.parent.mkdir()
        override.write_text("Existing override\n")
        self.run_setup("--apply", ok=False)
        self.assertFalse((self.home / ".pi").exists())

    def test_checkout_can_live_in_an_arbitrary_directory(self):
        checkout = Path(self.temp.name) / "checkout with spaces"
        for subdir in ("scripts", "instructions", "skills", "research"):
            shutil.copytree(REPO / "agentic" / subdir, checkout / "agentic" / subdir,
                            ignore=shutil.ignore_patterns("__pycache__"))
        result = subprocess.run(
            [sys.executable, str(checkout / "agentic/scripts/setup.py"),
             "--home", str(self.home), "--client", "claude", "--apply"],
            env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.home / ".claude/CLAUDE.md").resolve(),
                         checkout / "agentic/instructions/AGENTS.md")
        self.assertTrue((self.home / ".claude/skills/visual-explainer").is_dir())

    def test_parent_file_is_reported_before_changes(self):
        (self.home / ".agents").write_text("not a directory")
        self.run_setup("--apply", ok=False)
        self.assertFalse((self.home / ".pi").exists())


if __name__ == "__main__":
    unittest.main()
