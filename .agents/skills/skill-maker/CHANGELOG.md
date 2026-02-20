# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 20 Feb 2026 19:55

### Added

- `references/troubleshooting.md` - Common issues and solutions for skill creation
- Anti-Patterns section to `references/skill-concepts.md` with 10 common mistakes to avoid
- Mode selection guidance to SKILL.md Step 3 (regular vs minimal mode)
- `--comprehensive` flag and `--minimal` mode to Quick Reference table in SKILL.md

### Changed

- `scripts/package_skill.py`: Added `sys.path` handling for cross-directory execution
- `scripts/init_skill.py`: Added name length validation (max 40 characters, enforced)
- `scripts/quick_validate.py`: Added name length validation (max 40 characters)

### Fixed

- Package script now works when run from directories other than the script location
- Name length requirement (max 40 chars) is now enforced, not just documented

## [2.1.0] - 19 Feb 2026 01:40

### Added

- Overview section to SKILL.md summarizing the 6-step workflow at a glance
- `metadata.version` and `metadata.changelog` documented as required fields in skill anatomy tree (`references/skill-concepts.md`)
- `quick_validate.py`: validation for `metadata` block, `metadata.version` (semver format `\d+\.\d+\.\d+`), and `metadata.changelog` fields

### Changed

- Description pattern updated to commit-pro journey formula in SKILL.md, `references/skill-concepts.md` (Metadata Quality section + example), and both `init_skill.py` templates:
  - New formula: "This skill guides a complete, [adj] [domain] workflow from [START], through [MIDDLE], to [END]. This skill must be loaded (NON NEGOTIABLE) whenever user asks to [triggers]."
- `quick_validate.py`: fixed second-person false positives — inline double-quoted strings now stripped before pronoun check
- `quick_validate.py`: expanded structure pattern recognition to include `process`, `quick reference`, and `reference` keywords

## [2.0.1] - 17 Feb 2026 22:00

### Fixed

- Pre-quoted description in init_skill.py templates to produce valid YAML from the start
- Prevents agents from "fixing" YAML by adding quotes during edits
- Fixed table style formatting in multiple files for consistent markdown rendering

## [2.0.0] - 17 Feb 2026 21:07

### Breaking Changes

- **SKILL.md structure changed**: "About Skills" content moved to `references/skill-concepts.md`
  - Agents expecting skill anatomy docs in SKILL.md body must now load references
  - Structure patterns moved to `references/structure-patterns.md`
- **init_skill.py templates simplified**: Generated SKILL.md templates are now ~70% shorter
  - Verbose example files replaced with minimal placeholders
  - Use `--minimal` flag for even leaner output

### Added

- `references/` directory with self-documentation (skill now follows its own best practices)
- `references/skill-concepts.md` - Foundational knowledge about skills (moved from SKILL.md)
- `references/structure-patterns.md` - Detailed structure pattern guidance with decision tree
- `--minimal` flag to init_skill.py for creating skills without example placeholders
- `--comprehensive` flag to quick_validate.py for quality and style checks

### Changed

- SKILL.md refactored to procedural-only (~40% smaller)
  - Added Quick Reference table for common commands
  - Added References section linking to new reference files
- init_skill.py templates simplified:
  - SKILL_TEMPLATE reduced from ~87 lines to ~25 lines
  - Added minimal mode for bare-bones initialization
- quick_validate.py enhanced:
  - Split into validate_basic() and validate_comprehensive()
  - Comprehensive mode checks: description quality, writing style, structure patterns, resource references
  - Returns warnings and suggestions separately

### Fixed

- Skill now practices progressive disclosure principle it teaches (was violating it)

## [1.4.0] - 17 Feb 2026 20:09

### Added

- init_skill.py now generates CHANGELOG.md file automatically
- SKILL_TEMPLATE now includes metadata section with version and changelog fields

### Changed

- Simplified Structure section in template - now references skill-maker SKILL.md instead of duplicating content
- Removed verbose "Structuring This Skill" section - replaced with concise "Structure" section

## [1.3.0] - 17 Feb 2026 17:52

### Added

- Structure Patterns section in Step 4 with 4 common patterns:
  - Workflow-Based for sequential processes
  - Task-Based for tool collections
  - Reference/Guidelines for standards/specifications
  - Capabilities-Based for integrated systems

## [1.2.0] - 17 Feb 2026 17:23

### Changed

- Updated init_skill.py template to use the new description pattern formula
- Added TODO placeholder validation in quick_validate.py to prevent incomplete descriptions
- Ensures generated skills follow the same high-quality description pattern from the start

## [1.1.0] - 17 Feb 2026 16:39

### Changed

- Updated skill description to use stronger trigger pattern with "MUST" keyword
- Enhanced Metadata Quality guidelines with pattern formula and example
- Fixed pattern formula to use "for" connector instead of misleading "that"
- Removed redundant guidelines - now uses cleaner format: pattern → example → key points
- Ensures generated skills follow the same high-quality description pattern

## [1.0.0] - 17 Feb 2026 11:37

### Changed

- Renamed skill from `skill-creator` to `skill-maker` for universal agent compatibility
- Moved skill location from `.kilocode/skills/skill-creator` to `.agents/skills/skill-maker`
- Improved wording clarity and conciseness throughout SKILL.md:
  - Converted numbered lists to bullet points where sequence is not implied
  - Reduced wordiness in descriptions and instructions
  - Fixed path format from backslash to forward slash for cross-platform compatibility
  - Fixed typo `mnda.md` to `nda.md`
  - Improved consistency in writing style guidance
  - Removed redundant phrases and filler words

## [0.0.0] - 17 Feb 2026 10:00

### Added

- Initial release of skill-creator skill
- Comprehensive guide for creating effective skills
- Documentation of skill anatomy including:
  - SKILL.md structure with YAML frontmatter
  - Bundled resources organization (scripts/, references/, assets/)
- Progressive disclosure design principle documentation
- Step-by-step skill creation process:
  - Step 1: Understanding the skill with concrete examples
  - Step 2: Planning reusable skill contents
  - Step 3: Initializing the skill with init_skill.py script
  - Step 4: Editing the skill with proper writing style
  - Step 5: Packaging a skill with package_skill.py script
  - Step 6: Iteration workflow for improvements
- Guidelines for writing style using imperative/infinitive form
- Best practices for organizing references and avoiding duplication
- Examples of skill usage patterns and resource organization
