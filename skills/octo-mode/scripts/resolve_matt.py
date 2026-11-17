#!/usr/bin/env python3
"""Locate selected Matt method files without installing or executing them."""

import argparse
import hashlib
import json
import os
from pathlib import Path


MANIFEST = Path(__file__).resolve().parents[1] / "references" / "upstream.json"


def search_roots(project, explicit):
    roots = [Path(root).expanduser().resolve() for root in explicit]
    project = Path(project).expanduser().resolve()
    for parent in (project, *project.parents):
        roots.extend(parent / host / "skills" for host in (".agents", ".claude", ".codex"))
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    roots.extend((Path.home() / ".agents/skills", codex_home / "skills", Path.home() / ".claude/skills"))
    return list(dict.fromkeys(root.resolve() for root in roots))


def candidates(root, name, source_path):
    if root.name == name:
        yield root / "SKILL.md"
    yield root / name / "SKILL.md"
    yield root / source_path
    yield root / "skills" / name / "SKILL.md"
    for bucket in ("engineering", "productivity"):
        yield root / bucket / name / "SKILL.md"


def resolve_skill(name, metadata, roots):
    matches = []
    seen = set()
    for root in roots:
        for candidate in candidates(root, name, metadata["path"]):
            if not candidate.is_file():
                continue
            path = candidate.resolve()
            if path in seen:
                continue
            seen.add(path)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            matches.append({
                "path": str(path),
                "sha256": digest,
                "status": "baseline" if digest == metadata["sha256"] else "changed",
            })
    if not matches:
        return {"name": name, "status": "missing", "alternatives": []}
    return {"name": name, **matches[0], "alternatives": matches[1:]}


def main():
    manifest = json.loads(MANIFEST.read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=str(Path.cwd()), help="Target repository or working directory")
    parser.add_argument("--root", action="append", default=[], help="Trusted skill root, plugin directory, or upstream checkout; repeatable")
    parser.add_argument("skills", nargs="+", choices=sorted(manifest["methods"]))
    args = parser.parse_args()
    roots = search_roots(args.project, args.root)
    results = [resolve_skill(name, manifest["methods"][name], roots) for name in dict.fromkeys(args.skills)]
    print(json.dumps({
        "source": manifest["repository"],
        "baseline_commit": manifest["commit"],
        "skills": results,
        "searched_roots": [str(root) for root in roots],
    }, ensure_ascii=False, indent=2))
    return 1 if any(result["status"] == "missing" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
