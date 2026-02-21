#!/usr/bin/env python3
"""
Skill Validation Script - Quick and Comprehensive modes

Usage:
    quick_validate.py <skill_directory> [--comprehensive]

Options:
    --comprehensive    Run additional quality checks (writing style, structure)

Examples:
    quick_validate.py skills/public/my-skill
    quick_validate.py skills/public/my-skill --comprehensive
"""

import sys
import re
from pathlib import Path


def validate_basic(skill_path):
    """
    Basic validation - checks structural requirements.
    
    Returns: (valid: bool, message: str, details: dict)
    """
    skill_path = Path(skill_path).resolve()
    issues = []
    
    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", {}
    
    # Read content
    content = skill_md.read_text()
    
    # Check YAML frontmatter
    if not content.startswith('---'):
        return False, "No YAML frontmatter found", {}
    
    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", {}
    
    frontmatter = match.group(1)
    
    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter", {}
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter", {}
    if 'metadata:' not in frontmatter:
        return False, "Missing 'metadata' block in frontmatter", {}
    if 'version:' not in frontmatter:
        return False, "Missing 'metadata.version' in frontmatter", {}
    if 'changelog:' not in frontmatter:
        return False, "Missing 'metadata.changelog' in frontmatter", {}
    
    # Extract name for validation
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)", {}
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens", {}
        # Check name length (max 40 characters)
        if len(name) > 40:
            return False, f"Name '{name}' exceeds 40 characters ({len(name)} chars) - use a shorter name", {}

    # Extract and validate metadata.version (semver format)
    version_match = re.search(r'version:\s*(.+)', frontmatter)
    if version_match:
        version = version_match.group(1).strip()
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            return False, f"metadata.version '{version}' must follow semantic versioning (e.g., 1.0.0)", {}

    # Extract and validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)", {}
        # Check for TODO placeholder
        if '[TODO:' in description or '[TODO]' in description:
            return False, "Description contains TODO placeholder - must be completed", {}

    # Validate metadata.changelog path exists (relative to the parent of the skill directory)
    changelog_match = re.search(r'changelog:\s*(.+)', frontmatter)
    if changelog_match:
        changelog_rel = changelog_match.group(1).strip().strip('"').strip("'")
        if '\\' in changelog_rel:
            return False, f"metadata.changelog '{changelog_rel}' should use forward slashes (/)", {}
        changelog_path = skill_path.parent / changelog_rel
        if not changelog_path.exists():
            return False, f"metadata.changelog '{changelog_rel}' not found at: {changelog_path}", {}

    return True, "Basic validation passed", {'frontmatter': frontmatter, 'content': content}


def _find_line_matches(content: str, pattern: str, flags=0, max_hits: int = 5):
    """Return up to max_hits matches as (line_no, line_text) for regex pattern."""
    hits = []
    rx = re.compile(pattern, flags)
    for i, line in enumerate(content.splitlines(), start=1):
        if rx.search(line):
            hits.append((i, line.strip()))
            if len(hits) >= max_hits:
                break
    return hits


def _format_hits(hits):
    if not hits:
        return ""
    parts = []
    for ln, txt in hits:
        if len(txt) > 120:
            txt = txt[:117] + "..."
        parts.append(f"L{ln}: {txt}")
    return "; ".join(parts)


def validate_comprehensive(skill_path, content, frontmatter):
    """
    Comprehensive validation - checks quality and style.

    Returns: list of (severity, message) tuples where severity is one of:
      - 'error'   (must fix)
      - 'warning' (should fix)
      - 'info'    (nice to improve)
    """
    issues = []
    skill_path = Path(skill_path).resolve()

    # ----------------------------
    # 1) Description quality (frontmatter)
    # ----------------------------
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()

        if 'MUST' not in description and 'must' not in description:
            issues.append(('warning', "Description should use 'MUST' keyword for stronger trigger pattern"))

        if 'when' not in description.lower():
            issues.append(('warning', "Description should include trigger conditions (e.g., 'when...')"))

        if len(description) < 50:
            issues.append(('warning', f"Description may be too brief ({len(description)} chars) - consider adding more detail"))

    # ----------------------------
    # 2) Structure / required sections (SKILL.md body)
    # ----------------------------
    body_match = re.search(r'^---\n.*?\n---\n(.*)', content, re.DOTALL)
    body = body_match.group(1) if body_match else content

    h1 = re.findall(r'(?m)^#\s+.+', body)
    h2 = re.findall(r'(?m)^##\s+(.+)', body)

    if not h1:
        issues.append(('error', "Missing H1 title (# ...) in SKILL.md body"))

    sections = [s.strip().lower() for s in h2]

    if not any(s == 'overview' or s.startswith('overview') for s in sections):
        issues.append(('error', "Missing required section: '## Overview'"))

    non_overview = [s for s in sections if not s.startswith('overview')]
    if len(non_overview) < 1:
        issues.append(('error', "SKILL.md should include at least one section beyond '## Overview'"))

    has_pattern = any(
        any(k in s for k in ['workflow', 'tasks', 'guidelines', 'reference', 'capabilit', 'structure'])
        for s in sections
    )
    if not has_pattern:
        issues.append(('warning', "Skill doesn't show a recognizable structure pattern in headings (workflow/tasks/guidelines/capabilities/structure)"))

    # ----------------------------
    # 3) Placeholder / TODO gate (must be removed before packaging)
    # ----------------------------
    todo_hits = []
    todo_hits += _find_line_matches(content, r'\[TODO', flags=re.IGNORECASE)
    todo_hits += _find_line_matches(content, r'^\s*TODO:\s+', flags=re.IGNORECASE)

    if todo_hits:
        issues.append(('error', "Found TODO placeholder(s) - complete before packaging. " + _format_hits(todo_hits)))

    # ----------------------------
    # 4) Writing style hints (non-blocking)
    # ----------------------------
    body_stripped = re.sub(r'"[^"]*"', '', body, flags=re.MULTILINE)
    body_stripped = re.sub(r'^\s*>.*', '', body_stripped, flags=re.MULTILINE)
    second_person = re.findall(r"\b(you|your|yours|you'll|you'd)\b", body_stripped, re.IGNORECASE)
    if second_person:
        issues.append(('info', f"Found {len(second_person)} second-person pronoun(s) - consider using imperative form instead"))

    # ----------------------------
    # 5) Cross-platform path hygiene (prefer forward slashes in markdown)
    # ----------------------------
    backslash_hits = []
    backslash_hits += _find_line_matches(content, r'references\\', flags=re.IGNORECASE)
    backslash_hits += _find_line_matches(content, r'scripts\\', flags=re.IGNORECASE)
    backslash_hits += _find_line_matches(content, r'assets\\', flags=re.IGNORECASE)
    if backslash_hits:
        issues.append(('warning', "Found Windows-style backslashes in paths - prefer forward slashes (/). " + _format_hits(backslash_hits)))

    # ----------------------------
    # 6) Resource directories referenced
    # ----------------------------
    references_dir = skill_path / 'references'
    if references_dir.exists():
        ref_files = list(references_dir.glob('*.md'))
        if ref_files and ('references/' not in content and 'references\\' not in content):
            issues.append(('info', f"references/ exists with {len(ref_files)} file(s) but SKILL.md doesn't reference it"))

    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
        if scripts and ('scripts/' not in content and 'scripts\\' not in content):
            issues.append(('info', f"scripts/ exists with {len(scripts)} file(s) but SKILL.md doesn't reference it"))

    # ----------------------------
    # 7) External dependencies hygiene (non-blocking)
    # ----------------------------
    mentions_deps = re.search(r'\b(API key|apikey|token|environment variable|env var|MCP|OAuth)\b', content, re.IGNORECASE)
    has_deps_section = any('external dependenc' in s or 'dependency' in s for s in sections)
    if mentions_deps and not has_deps_section:
        issues.append(('warning', "Skill mentions external configuration but has no 'External Dependencies' section"))

    changelog = skill_path / 'CHANGELOG.md'
    if not changelog.exists():
        issues.append(('info', "No CHANGELOG.md found - consider adding one for version tracking"))

    return issues



def validate_skill(skill_path, comprehensive=False):
    """
    Main validation function.

    Args:
        skill_path: Path to skill directory
        comprehensive: If True, run additional quality checks

    Returns: (valid: bool, message: str)
    """
    valid, message, details = validate_basic(skill_path)
    if not valid:
        return False, message

    if comprehensive:
        issues = validate_comprehensive(skill_path, details.get('content', ''), details.get('frontmatter', ''))
        if issues:
            errors = [i for i in issues if i[0] == 'error']
            warnings = [i for i in issues if i[0] == 'warning']
            infos = [i for i in issues if i[0] == 'info']

            lines = []
            if errors:
                lines.append("Errors:")
                for _, msg in errors:
                    lines.append(f"  - {msg}")
            if warnings:
                lines.append("Warnings:")
                for _, msg in warnings:
                    lines.append(f"  - {msg}")
            if infos:
                lines.append("Suggestions:")
                for _, msg in infos:
                    lines.append(f"  - {msg}")

            if errors:
                return False, f"Comprehensive validation failed with {len(errors)} error(s):\n" + "\n".join(lines)

            if warnings:
                return True, f"Validation passed, but {len(warnings)} warning(s) found:\n" + "\n".join(lines)

            return True, f"Validation passed with {len(infos)} suggestion(s):\n" + "\n".join(lines)

    return True, "Skill is valid!"


def main():
    # Parse arguments
    args = sys.argv[1:]
    comprehensive = '--comprehensive' in args
    if comprehensive:
        args.remove('--comprehensive')
    
    if len(args) != 1:
        print("Usage: quick_validate.py <skill_directory> [--comprehensive]")
        print("\nOptions:")
        print("  --comprehensive    Run additional quality checks (writing style, structure)")
        print("\nExamples:")
        print("  quick_validate.py skills/public/my-skill")
        print("  quick_validate.py skills/public/my-skill --comprehensive")
        sys.exit(1)
    
    skill_path = args[0]
    
    if comprehensive:
        print(f"Running comprehensive validation on: {skill_path}")
    else:
        print(f"Running quick validation on: {skill_path}")
    
    valid, message = validate_skill(skill_path, comprehensive)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()