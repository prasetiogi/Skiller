#!/usr/bin/env python3
"""
Smoke Test Runner - Automated functional smoke gate for a skill folder.

Usage:
    smoke_test.py <path/to/skill-folder>

What it does:
  1) Runs comprehensive validation (fails on errors)
  2) Runs lightweight heuristics (non-blocking warnings)

This does NOT execute external tools. It is a quick gate before manual testing.
"""

import sys
import re
from pathlib import Path

# Allow running from anywhere
sys.path.insert(0, str(Path(__file__).parent))
from quick_validate import validate_skill


def _count_example_prompts(skill_md_text: str) -> int:
    """Heuristic: count quoted example prompts or bullet prompts."""
    # Count lines that look like prompts in quotes or bullets
    quoted = re.findall(r"['\"]{1}[^'\"]{8,}['\"]{1}", skill_md_text)
    bullets = re.findall(r"(?m)^\s*[-*]\s+.+\?$", skill_md_text)
    return max(len(quoted), 0) + max(len(bullets), 0)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: smoke_test.py <path/to/skill-folder>")
        sys.exit(1)

    skill_path = Path(args[0]).resolve()
    print(f"🧪 Smoke testing: {skill_path}\n")

    valid, message = validate_skill(skill_path, comprehensive=True)
    if not valid:
        print("❌ FAIL\n")
        print(message)
        sys.exit(2)

    print("✅ Validation gate passed\n")
    if "Warnings:" in message or "Suggestions:" in message:
        print(message)
        print()

    # Lightweight heuristic checks
    skill_md = skill_path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8", errors="replace")

    prompt_count = _count_example_prompts(text)
    if prompt_count < 2:
        print("⚠️  Warning: fewer than 2 example-like prompts detected in SKILL.md.")
        print("   Consider adding 2+ concrete example prompts to improve triggering and usability.\n")

    print("✅ Smoke test complete.")
    print("Next: run 2–3 manual end-to-end use cases (see references/testing-template.md).")


if __name__ == "__main__":
    main()
