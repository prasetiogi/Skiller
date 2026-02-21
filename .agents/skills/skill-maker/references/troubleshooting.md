# Troubleshooting Guide

This document covers common issues encountered when creating skills and their solutions.

## Validation Errors

### "SKILL.md not found"

**Cause:** Running validation from wrong directory or missing SKILL.md file.

**Solution:**
- Ensure SKILL.md exists in the skill directory
- Run validation with the correct path: `quick_validate.py path/to/skill-name`

### "No YAML frontmatter found"

**Cause:** SKILL.md missing the required YAML header.

**Solution:**
Add frontmatter at the start of SKILL.md:
```yaml
---
name: skill-name
description: "Description here"
metadata:
  version: 1.0.0
  changelog: skill-name/CHANGELOG.md
---
```

### "Name 'X' should be hyphen-case"

**Cause:** Skill name contains invalid characters.

**Solution:**
- Use only lowercase letters, digits, and hyphens
- Example: `my-skill-name` not `My_Skill_Name`

### "Name 'X' exceeds 40 characters"

**Cause:** Skill name is too long.

**Solution:**
- Shorten the name to 40 characters or less
- Use abbreviations if necessary
- Example: `pdf-rotator` instead of `pdf-document-rotation-utility`

### "Description contains TODO placeholder"

**Cause:** SKILL.md was created from template but not customized.

**Solution:**
Replace the TODO placeholder with a real description following the pattern:
```
This skill guides a complete, [adjective] [domain] workflow from [START], through [MIDDLE], to [END]. This skill must be loaded (NON NEGOTIABLE) whenever user asks to [triggers].
```

### "metadata.version must follow semantic versioning"

**Cause:** Version string doesn't match X.Y.Z format.

**Solution:**
- Use format: `major.minor.patch` (e.g., `1.0.0`, `2.1.3`)
- Increment major for breaking changes
- Increment minor for new features
- Increment patch for bug fixes

## Script Errors

### "ModuleNotFoundError: No module named 'quick_validate'"

**Cause:** Running package_skill.py from outside the scripts directory.

**Solution:**
Run from the skill-maker directory or use the full path:
```bash
cd .agents/skills/skill-maker/scripts
python package_skill.py path/to/skill
```

### "Error: Skill directory already exists"

**Cause:** Trying to initialize a skill that already exists.

**Solution:**
- Remove the existing directory first, or
- Use a different skill name, or
- Edit the existing skill instead of creating new

### "Permission denied" when running scripts

**Cause:** Script doesn't have execute permission.

**Solution:**
```bash
chmod +x scripts/init_skill.py
chmod +x scripts/package_skill.py
chmod +x scripts/quick_validate.py
```

### Cross-platform path issues (Windows vs Linux)

**Symptoms:**

- Links in SKILL.md use backslashes (e.g., `references\foo.md`) and fail in some environments
- Scripts behave differently across OSes (path joins, line endings)

**Fixes:**

- Use **forward slashes** in markdown links: `references/foo.md`
- In Python scripts, use `pathlib.Path` for all path operations
- If a script must print paths, print resolved paths for clarity

## Content Issues

### Skill not triggering when expected

**Possible causes:**

1. **Description lacks trigger keywords**
   - Add "must be loaded (NON NEGOTIABLE)" phrase
   - Include specific trigger conditions with "when"

2. **Description is too vague**
   - Be specific about what the skill does
   - Include the full journey: from → through → to

3. **Name doesn't match user intent**
   - Choose a name that reflects common terminology

### Agent not following skill instructions

**Possible causes:**

1. **SKILL.md is too long**
   - Move detailed content to references/
   - Keep SKILL.md under 5,000 words

2. **Instructions are ambiguous**
   - Use imperative form ("Do X" not "You should do X")
   - Be explicit about required vs optional steps

3. **Missing context in references**
   - Add decision trees for complex choices
   - Include concrete examples

### Skill produces inconsistent results

**Possible causes:**

1. **Missing guardrails**
   - Add validation steps
   - Include verification criteria

2. **Too much flexibility in workflow**
   - Add decision points with clear conditions
   - Specify when to skip steps

3. **Missing error handling guidance**
   - Add troubleshooting section to SKILL.md
   - Document common failure modes

### User feedback is unclear or contradictory

**Symptoms:**

- Requirements keep shifting
- The user cannot provide concrete examples

**Solution:**

- Propose 3–5 representative prompts and ask the user to confirm which are correct.
- Reduce ambiguity with forced choices:
  - "Should this skill focus on A, B, or both?"
  - "Which output format is required: X or Y?"
- Capture constraints early (inputs, outputs, non-goals) and treat them as acceptance criteria.

### Skill depends on external configuration (API keys, credentials, MCP tools)

**Best practices:**

- Never hardcode secrets in a skill.
- Document required environment variables in SKILL.md.
- Provide safe defaults / failure messaging (e.g., "If API key missing, stop and request it").
- If the skill depends on another skill, document that dependency explicitly in SKILL.md.

## Expected Script Outputs (Typical)

Use these as a sanity check when running tooling.

- `init_skill.py ...` prints "Created SKILL.md" and "Created CHANGELOG.md" and ends with "Skill '<name>' initialized".
- `quick_validate.py <dir>` prints "Skill is valid!" on success.
- `quick_validate.py <dir> --comprehensive` may print "Warnings:" and/or "Suggestions:".
- `package_skill.py <dir>` prints "Validating skill..." then "Successfully packaged".

## Packaging Issues

### "Validation failed" during packaging

**Cause:** Skill doesn't pass validation checks.

**Solution:**
1. Run `quick_validate.py --comprehensive` to see all issues
2. Fix each error/warning
3. Run validation again before packaging

### Zip file missing files

**Cause:** Files not properly included in skill directory.

**Solution:**
- Ensure all files are inside the skill directory
- Check that SKILL.md references all bundled resources
- Verify file paths match references in SKILL.md

## Best Practice Reminders

1. **Always test the skill** after creation with real use cases
2. **Version properly** - update version and CHANGELOG for each change
3. **Keep it lean** - move detailed content to references/
4. **Be specific** - vague descriptions lead to poor triggering
5. **Iterate** - improve based on real-world performance