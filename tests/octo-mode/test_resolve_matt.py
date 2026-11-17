import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[2] / "skills/octo-mode"
SCRIPT = SKILL / "scripts/resolve_matt.py"
spec = importlib.util.spec_from_file_location("resolve_matt", SCRIPT)
resolver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resolver)


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.content = b"---\nname: tdd\n---\nBaseline method.\n"
        self.metadata = {
            "path": "skills/engineering/tdd/SKILL.md",
            "sha256": hashlib.sha256(self.content).hexdigest(),
        }

    def write_method(self, path, content=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.content if content is None else content)
        return path

    def test_flat_install_is_resolved_with_baseline_status(self):
        path = self.write_method(self.root / "tdd/SKILL.md")
        result = resolver.resolve_skill("tdd", self.metadata, [self.root])
        self.assertEqual(result["path"], str(path))
        self.assertEqual(result["status"], "baseline")

    def test_checkout_and_bucket_roots_are_supported(self):
        path = self.write_method(self.root / self.metadata["path"])
        for root in (self.root, self.root / "skills", path.parent):
            with self.subTest(root=root):
                self.assertEqual(resolver.resolve_skill("tdd", self.metadata, [root])["path"], str(path))

    def test_changed_method_is_visible(self):
        self.write_method(self.root / "tdd/SKILL.md", b"A different tdd implementation")
        self.assertEqual(resolver.resolve_skill("tdd", self.metadata, [self.root])["status"], "changed")

    def test_precedence_keeps_alternate_sources_visible(self):
        preferred = self.write_method(self.root / "project/tdd/SKILL.md")
        alternate = self.write_method(self.root / "global/tdd/SKILL.md", b"Other skill pack")
        result = resolver.resolve_skill("tdd", self.metadata, [preferred.parents[1], alternate.parents[1]])
        self.assertEqual(result["path"], str(preferred))
        self.assertEqual(result["alternatives"][0]["path"], str(alternate))
        self.assertEqual(result["alternatives"][0]["status"], "changed")

    def test_symlinks_are_not_duplicate_sources(self):
        path = self.write_method(self.root / "actual/tdd/SKILL.md")
        (self.root / "alias").symlink_to(self.root / "actual", target_is_directory=True)
        result = resolver.resolve_skill("tdd", self.metadata, [self.root / "alias", self.root / "actual"])
        self.assertEqual(result["path"], str(path))
        self.assertEqual(result["alternatives"], [])

    def test_missing_dependency_is_explicit(self):
        result = resolver.resolve_skill("tdd", self.metadata, [self.root])
        self.assertEqual(result["status"], "missing")
        self.assertNotIn("path", result)

    def test_explicit_root_precedes_nearest_project_and_parent(self):
        project = self.root / "repo/nested"
        roots = resolver.search_roots(project, [self.root / "plugin"])
        self.assertEqual(roots[0], self.root / "plugin")
        self.assertLess(roots.index(project / ".agents/skills"), roots.index(self.root / "repo/.agents/skills"))

    def test_cli_reports_changed_source_and_rejects_unknown_method(self):
        path = self.write_method(self.root / "tdd/SKILL.md")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "tdd"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        selected = json.loads(result.stdout)["skills"][0]
        self.assertEqual(selected["path"], str(path))
        self.assertEqual(selected["status"], "changed")
        result = subprocess.run([sys.executable, str(SCRIPT), "invented-skill"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
