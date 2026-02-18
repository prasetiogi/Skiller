# Changelog

## [1.1.0] - 2026-02-19

### Changed
- Expanded skill trigger description to cover `git commit` and `any commit related task` in addition to `commit`, improving trigger coverage across model variants
- Changed reference loading from lazy (per-step) to mandatory upfront — both `references/atomic-commit-principles.md` and `references/conventional-commits.md` must be loaded before the workflow begins, preventing models from skipping the split decision reference

## [1.0.0] - 2026-02-18

### Added
- Initial release of the `commit-pro` skill
- 4-step workflow: deep change analysis, atomic commit splitting, message writing, and execution
- Pre-flight check to validate repository state before beginning
- Step 1: Deep Change Analysis using git status, git diff, git log, read_file, and search_files
- Step 2: Logical Grouping with atomic commit principles and split decision tree
- Step 3: Dual-file commit message strategy (.git/COMMITS.TXT for planning, .git/COMMIT_MSG_N for execution)
- Step 4: Per-group staging with git commit -F and post-execution verification
- Quality gates with explicit self-check questions at each step
- Critical constraints block enforcing: no `git add .`, mandatory scope, mandatory body
- `references/conventional-commits.md` — Angular CC spec, type glossary, scope guidelines, custom rules, body writing guide, 3 good examples, 3 anti-patterns
- `references/atomic-commit-principles.md` — split decision tree, grouping rules table, 5 common scenarios, git add -p edge case, commit ordering guidance
