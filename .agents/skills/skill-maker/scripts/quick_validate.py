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
    skill_path = Path(skill_path)
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

    return True, "Basic validation passed", {'frontmatter': frontmatter, 'content': content}


def validate_comprehensive(skill_path, content, frontmatter):
    """
    Comprehensive validation - checks quality and style.
    
    Returns: list of (severity, message) tuples
    """
    issues = []
    skill_path = Path(skill_path)
    
    # 1. Check description quality
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        
        # Check for MUST keyword (strong trigger pattern)
        if 'MUST' not in description and 'must' not in description:
            issues.append(('warning', "Description should use 'MUST' keyword for stronger trigger pattern"))
        
        # Check for trigger conditions
        if 'when' not in description.lower():
            issues.append(('warning', "Description should include trigger conditions ('when...')"))
        
        # Check minimum length
        if len(description) < 50:
            issues.append(('warning', f"Description may be too brief ({len(description)} chars) - consider adding more detail"))
    
    # 2. Check writing style
    body_match = re.search(r'^---\n.*?\n---\n(.*)', content, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        
        # Check for second-person pronouns (should use imperative form)
        # Strip quoted content (inline double-quoted strings and blockquotes) before checking
        body_stripped = re.sub(r'"[^"]*"', '', body, flags=re.MULTILINE)
        body_stripped = re.sub(r'^\s*>.*', '', body_stripped, flags=re.MULTILINE)
        second_person = re.findall(r'\b(you|your|yours|you\'ll|you\'d)\b', body_stripped, re.IGNORECASE)
        if second_person:
            issues.append(('info', f"Found {len(second_person)} second-person pronoun(s) - consider using imperative form instead"))
        
        # Check for TODO placeholders in body
        todos = re.findall(r'\[TODO[^\]]*\]', body, re.IGNORECASE)
        if todos:
            issues.append(('warning', f"Found {len(todos)} TODO placeholder(s) in body - complete before packaging"))
    
    # 3. Check structure
    sections = re.findall(r'^##\s+(.+)', content, re.MULTILINE)
    
    # Check for Overview section
    if not any('overview' in s.lower() for s in sections):
        issues.append(('info', "Consider adding an 'Overview' section for clarity"))
    
    # Check for common structure patterns
    has_workflow = any('step' in s.lower() or 'workflow' in s.lower() or 'process' in s.lower() for s in sections)
    has_tasks = any('task' in s.lower() or 'quick start' in s.lower() or 'quick reference' in s.lower() for s in sections)
    has_capabilities = any('capabilit' in s.lower() or 'feature' in s.lower() for s in sections)
    has_guidelines = any('guideline' in s.lower() or 'standard' in s.lower() or 'spec' in s.lower() or 'reference' in s.lower() for s in sections)
    
    if not (has_workflow or has_tasks or has_capabilities or has_guidelines):
        issues.append(('info', "Skill doesn't follow common structure patterns - see skill-maker references/structure-patterns.md"))
    
    # 4. Check for references directory
    references_dir = skill_path / 'references'
    if references_dir.exists():
        ref_files = list(references_dir.glob('*.md'))
        if ref_files:
            # Check if SKILL.md references the references directory
            if 'references/' not in content and 'references\\' not in content:
                issues.append(('info', f"references/ directory exists with {len(ref_files)} file(s) but SKILL.md doesn't reference it"))
    
    # 5. Check for scripts directory
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
        if scripts:
            # Check if SKILL.md references the scripts directory
            if 'scripts/' not in content and 'scripts\\' not in content:
                issues.append(('info', f"scripts/ directory exists with {len(scripts)} file(s) but SKILL.md doesn't reference it"))
    
    # 6. Check CHANGELOG.md
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
    # Basic validation
    valid, message, details = validate_basic(skill_path)
    if not valid:
        return False, message
    
    # Comprehensive validation
    if comprehensive:
        issues = validate_comprehensive(skill_path, details.get('content', ''), details.get('frontmatter', ''))
        
        if issues:
            # Format issues
            issue_lines = []
            warnings = [i for i in issues if i[0] == 'warning']
            infos = [i for i in issues if i[0] == 'info']
            
            if warnings:
                issue_lines.append("Warnings:")
                for severity, msg in warnings:
                    issue_lines.append(f"  - {msg}")
            
            if infos:
                issue_lines.append("Suggestions:")
                for severity, msg in infos:
                    issue_lines.append(f"  - {msg}")
            
            if warnings:
                return True, f"Basic validation passed, but {len(warnings)} warning(s) found:\n" + "\n".join(issue_lines)
            else:
                return True, f"Validation passed with {len(infos)} suggestion(s):\n" + "\n".join(issue_lines)
    
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