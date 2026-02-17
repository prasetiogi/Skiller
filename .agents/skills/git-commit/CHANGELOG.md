# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 17 Feb 2026

### Fixed

- Updated version to 0.0.3
- Enhanced COMMIT.TXT workflow documentation
- Added specific guidance to use `write_to_file` tool for creating/editing `.git/COMMIT.TXT` file
- Improved clarity on file-based commit message creation process to fix drifting on some agent

## [0.0.2] - 17 Feb 2026

### Changed

- Updated description to explicitly remind agent to load skill before commit
- Incremented version to 0.0.2

## [0.0.1] - 17 Feb 2026

### Added

- Initial release of git-commit skill
- Commit message format following conventional commits standard
- Types: feat, fix, refactor, chore, docs, style, test, perf, ci, build, revert
- Breaking changes documentation with `!` notation
- Professional commit message structure with "What" and "Why" sections
- Step-by-step workflow for creating commits
- Examples for feature, fix, and breaking change commits
- Guidelines for using COMMIT.TXT file to avoid message truncation
- Verification commands (git status, git log)
