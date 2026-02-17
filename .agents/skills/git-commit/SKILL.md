---
name: git-commit
description: This skill should be used when creating commit messages following conventional commits standard.
metadata:
  version: 0.0.1
  changelog: git-commit/CHANGELOG.md
---

# Git Commit

This skill standardizes the commit message creation process following conventional commits standard.

## Commit Message Format

Use the conventional commits format:

```
type(scope)!: description
```

### Types

- **feat** - New feature
- **fix** - Bug fix
- **refactor** - Code refactoring
- **chore** - Maintenance tasks
- **docs** - Documentation changes
- **style** - Code style changes
- **test** - Test changes
- **perf** - Performance improvements
- **ci** - CI/CD changes
- **build** - Build system changes
- **revert** - Revert changes

### Breaking Changes

Add `!` after scope to indicate breaking changes:

```
refactor(skill)!: description
```

Always include `BREAKING CHANGE:` section in the body:

```
BREAKING CHANGE: Description of what changed
- Old: previous behavior
- New: new behavior
```

## Professional Commit Messages

### Structure

1. **Subject line** - Keep under 72 characters
2. **Body** - Use "What" and "Why" sections
3. **Breaking changes** - If applicable

### Example

```
refactor(skill)!: rename skill-creator to skill-maker

What:
- Renamed skill from skill-creator to skill-maker
- Moved from .kilocode/skills/ to .agents/skills/ directory

Why:
- Original name was platform-specific
- The .agents/ directory is the standard for universal agents

BREAKING CHANGE: Skill path changed
- Old: .kilocode/skills/skill-creator
- New: .agents/skills/skill-maker
```

### Guidelines

- Use imperative mood (e.g., "Add feature" not "Added feature")
- Reference issues/tickets when applicable
- Explain what changed and why

## Workflow

### Step 1: Analyze Changes

Review the changes to commit:

```bash
git status
git diff --stat
```

### Step 2: Determine Type

Choose the appropriate type based on the changes:
- New feature → `feat`
- Bug fix → `fix`
- Code changes without new features → `refactor`
- Documentation → `docs`
- Maintenance → `chore`

### Step 3: Determine Scope

The scope is optional but recommended. Common scopes:
- `skill` - Skills-related changes
- `docs` - Documentation changes
- `ci` - CI/CD changes
- `build` - Build system changes

### Step 4: Write Subject Line

- Keep under 72 characters
- Use lowercase for description
- No period at the end

### Step 5: Write Body (Optional)

Include "What" and "Why" sections:
- What: Describe what changed
- Why: Explain the reason for the change

### Step 6: Breaking Changes

If the change is breaking:
- Add `!` after scope in subject
- Include `BREAKING CHANGE:` section in body
- Provide migration guidance

## Executing Commit

### Using COMMIT.TXT File

To avoid message truncation, use a file instead of `-m` flag:

```bash
# Write commit message to .git/COMMIT.TXT
git add .
git commit -F .git/COMMIT.TXT
```

### Verification

After commit, verify with:

```bash
git status
git log --oneline -3
```

## Examples

### Feature Commit

```
feat(auth): add login endpoint

What:
- Added POST /api/login endpoint
- Implemented JWT token generation

Why:
- Required for user authentication flow
```

### Fix Commit

```
fix(api): handle null response from external API

What:
- Added null check for API responses
- Return empty array when API returns null

Why:
- Prevented crash when external API returns null
- Improved error handling
```

### Breaking Change Commit

```
refactor(config)!: change config file format

What:
- Changed from JSON to YAML configuration
- Updated config loading logic

Why:
- YAML is more readable and supports comments

BREAKING CHANGE: Config file format changed
- Old: config.json
- New: config.yaml
```
