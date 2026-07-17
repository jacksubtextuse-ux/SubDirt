"""Package a skill folder into a .skill file (zip) for Cowork "Install from file".

Usage:
    python tools/package_skill.py skills/student-housing-entitlements [out_dir]

Zips the folder with the skill directory name as the zip root (matching the layout Cowork
expects: <name>/SKILL.md, <name>/references/..., <name>/scripts/...). Output defaults to
dist/<name>.skill.
"""
import sys
import zipfile
from pathlib import Path

EXCLUDE_SUFFIXES = {".pyc"}
EXCLUDE_NAMES = {"__pycache__", ".DS_Store", "SPEC.md"}


def package(skill_dir: Path, out_dir: Path) -> Path:
    if not (skill_dir / "SKILL.md").is_file():
        sys.exit(f"error: {skill_dir} has no SKILL.md — not a packageable skill (SPEC-only?)")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{skill_dir.name}.skill"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(skill_dir.rglob("*")):
            if p.is_dir():
                continue
            if p.name in EXCLUDE_NAMES or p.suffix in EXCLUDE_SUFFIXES:
                continue
            if any(part in EXCLUDE_NAMES for part in p.parts):
                continue
            z.write(p, Path(skill_dir.name) / p.relative_to(skill_dir))
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    skill = Path(sys.argv[1]).resolve()
    dist = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else skill.parents[1] / "dist"
    result = package(skill, dist)
    print(f"packaged: {result}")
