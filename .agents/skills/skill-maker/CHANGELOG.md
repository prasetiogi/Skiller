# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
