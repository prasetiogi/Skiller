#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable zip file of a skill folder

Usage:
    package_skill.py <path/to/skill-folder> [output-directory] [--comprehensive]

Example:
    package_skill.py skills/public/my-skill
    package_skill.py skills/public/my-skill ./dist
    package_skill.py skills/public/my-skill ./dist --comprehensive
"""

import sys
import zipfile
from pathlib import Path

# Add parent directory to path for imports when running from different directory
sys.path.insert(0, str(Path(__file__).parent))
from quick_validate import validate_skill


def package_skill(skill_path, output_dir=None, comprehensive=False):
    """
    Package a skill folder into a zip file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the zip file (defaults to current directory)

    Returns:
        Path to the created zip file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path, comprehensive=comprehensive)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    zip_filename = output_path / f"{skill_name}.zip"

    # Create the zip file
    try:
        def should_include(p: Path) -> bool:
            # Exclude common non-source artifacts
            if '__pycache__' in p.parts:
                return False
            if p.suffix in {'.pyc', '.pyo'}:
                return False
            if p.name in {'.DS_Store'}:
                return False
            return True

        files = [p for p in skill_path.rglob('*') if p.is_file() and should_include(p)]
        total = len(files)
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, file_path in enumerate(files, start=1):
                # Calculate the relative path within the zip (includes the skill folder name)
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added ({i}/{total}): {arcname}")

        print(f"\n✅ Successfully packaged skill to: {zip_filename}")
        return zip_filename

    except Exception as e:
        print(f"❌ Error creating zip file: {e}")
        return None


def main():
    args = sys.argv[1:]
    comprehensive = '--comprehensive' in args
    if comprehensive:
        args.remove('--comprehensive')

    if len(args) < 1:
        print("Usage: package_skill.py <path/to/skill-folder> [output-directory] [--comprehensive]")
        print("\nExample:")
        print("  package_skill.py skills/public/my-skill")
        print("  package_skill.py skills/public/my-skill ./dist")
        print("  package_skill.py skills/public/my-skill ./dist --comprehensive")
        sys.exit(1)

    skill_path = args[0]
    output_dir = args[1] if len(args) > 1 else None

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    if comprehensive:
        print("   Validation: comprehensive")

    result = package_skill(skill_path, output_dir, comprehensive=comprehensive)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
