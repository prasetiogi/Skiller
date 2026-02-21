#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--minimal]

Options:
    --minimal    Create only essential files (no example placeholders)

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private --minimal
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path
from datetime import datetime
import re


SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: This skill guides a complete, structured workflow from [START], through [MIDDLE], to [END]. This skill must be loaded (NON NEGOTIABLE) whenever user asks to [trigger1], [trigger2], or [catch-all].]"
metadata:
  version: 0.0.0
  changelog: {skill_name}/CHANGELOG.md
---

# {skill_title}

## Overview

TODO: Replace with 1–2 sentences explaining what this skill enables.

## When to Use

- Trigger phrases (examples): TODO
- Out of scope: TODO

## External Dependencies

- None.
- If required, list: API keys, environment variables, MCP tools, OS-specific paths, network access.

## Structure

Choose ONE pattern and structure the rest of the doc accordingly (see skill-maker `references/structure-patterns.md`):

- Workflow-Based
- Task-Based
- Reference/Guidelines
- Capabilities-Based

## Main Content

TODO: Add the actual workflow/tasks/guidelines/capabilities, including:
- 2+ concrete example prompts
- at least 1 verification step (expected output / invariants / success criteria)
- at least 1 failure mode + what to do next

## Resources

{resources_section}
"""

SKILL_TEMPLATE_MINIMAL = """---
name: {skill_name}
description: "[TODO: This skill guides a complete, structured workflow from [START], through [MIDDLE], to [END]. This skill must be loaded (NON NEGOTIABLE) whenever user asks to [trigger1], [trigger2], or [catch-all].]"
metadata:
  version: 0.0.0
  changelog: {skill_name}/CHANGELOG.md
---

# {skill_title}

## Overview

TODO: Replace with 1–2 sentences explaining what this skill enables.

## External Dependencies

- None.
- If required, list: API keys, environment variables, MCP tools, OS-specific paths, network access.

## Main Content

TODO: Add sections based on the chosen structure pattern.
"""

CHANGELOG_TEMPLATE = """# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.0] - {datetime}

### Added

- Initial release of {skill_name} skill
- [TODO: Add initial features/capabilities]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""Helper script for {skill_name}"""

def main():
    # TODO: Implement script logic
    pass

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference for {skill_title}

[TODO: Add reference documentation - API docs, schemas, detailed guides]
"""

EXAMPLE_ASSET_PLACEHOLDER = "# Place asset files here (templates, images, fonts, etc.)\n"


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path, minimal=False):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created
        minimal: If True, create only essential files

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    
    if minimal:
        resources_section = "[TODO: Add scripts/, references/, or assets/ as needed]"
        skill_content = SKILL_TEMPLATE_MINIMAL.format(
            skill_name=skill_name,
            skill_title=skill_title,
            resources_section=resources_section
        )
    else:
        resources_section = """This skill includes example resource directories. Delete unneeded directories.

- **scripts/** - Executable code (Python/Bash/etc.)
- **references/** - Documentation to load into context
- **assets/** - Files used in output (templates, images)"""
        skill_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title,
            resources_section=resources_section
        )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("Created SKILL.md")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    # Create CHANGELOG.md from template
    current_datetime = datetime.now().strftime("%d %b %Y %H:%M")
    changelog_content = CHANGELOG_TEMPLATE.format(
        skill_name=skill_name,
        datetime=current_datetime
    )

    changelog_path = skill_dir / 'CHANGELOG.md'
    try:
        changelog_path.write_text(changelog_content)
        print("Created CHANGELOG.md")
    except Exception as e:
        print(f"Error creating CHANGELOG.md: {e}")
        return None

    # Create resource directories
    try:
        # Always create directories structure (even if minimal)
        scripts_dir = skill_dir / 'scripts'
        references_dir = skill_dir / 'references'
        assets_dir = skill_dir / 'assets'
        
        scripts_dir.mkdir(exist_ok=True)
        references_dir.mkdir(exist_ok=True)
        assets_dir.mkdir(exist_ok=True)
        
        if not minimal:
            # Create example files
            example_script = scripts_dir / 'example.py'
            example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
            example_script.chmod(0o755)
            print("Created scripts/example.py")

            example_reference = references_dir / 'reference.md'
            example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
            print("Created references/reference.md")

            example_asset = assets_dir / '.gitkeep'
            example_asset.write_text(EXAMPLE_ASSET_PLACEHOLDER)
            print("Created assets/ directory")
        else:
            print("Created scripts/, references/, assets/ directories (empty)")
            
    except Exception as e:
        print(f"Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\nSkill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    steps = []
    steps.append("Edit SKILL.md - complete TODO items and update description")
    steps.append("Update CHANGELOG.md with initial features")
    if not minimal:
        steps.append("Customize or delete example files in scripts/, references/, assets/")
    else:
        steps.append("Add scripts/, references/, assets/ as needed (or delete unused dirs)")
    steps.append("Run quick_validate.py --comprehensive before packaging")
    for i, s in enumerate(steps, start=1):
        print(f"{i}. {s}")

    return skill_dir


def main():
    # Parse arguments
    args = sys.argv[1:]
    minimal = '--minimal' in args
    if minimal:
        args.remove('--minimal')
    
    if len(args) < 3 or args[1] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path> [--minimal]")
        print("\nOptions:")
        print("  --minimal    Create only essential files (no example placeholders)")
        print("\nSkill name requirements:")
        print("  - Hyphen-case identifier (e.g., 'data-analyzer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 40 characters")
        print("  - Must match directory name exactly")
        print("\nExamples:")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private --minimal")
        sys.exit(1)

    skill_name = args[0]
    path = args[2]

    # Validate skill name length
    if len(skill_name) > 40:
        print(f"Error: Skill name exceeds 40 characters ({len(skill_name)} chars)")
        print("  Use a shorter name or abbreviate")
        sys.exit(1)

    # Validate skill name format (hyphen-case)
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        print(f"Error: Skill name '{skill_name}' should be hyphen-case (lowercase letters, digits, and hyphens only)")
        sys.exit(1)
    if skill_name.startswith('-') or skill_name.endswith('-') or '--' in skill_name:
        print(f"Error: Skill name '{skill_name}' cannot start/end with hyphen or contain consecutive hyphens")
        sys.exit(1)

    print(f"Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    if minimal:
        print("   Mode: minimal")
    print()

    result = init_skill(skill_name, path, minimal)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
