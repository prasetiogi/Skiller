# Skill Testing Template

Use this template for a lightweight functional smoke test before packaging a skill.

## Goal

Validate that a *fresh agent* can:

- Load the skill at the right time (triggering)
- Follow SKILL.md instructions without missing context
- Use bundled resources correctly (scripts/references/assets)
- Produce outputs that match expectations

## Setup

- Use a **fresh agent context** (no prior conversation state).
- Ensure any required environment/config is present:
  - API keys (env vars)
  - Credentials or tool access
  - OS-specific dependencies

## Test Cases (2–5 total)

Create 2–5 cases that cover the skill’s most common usage patterns.

For each case, fill this:

### Case N: <short name>

- **User prompt:**
  - `<paste the exact prompt that should trigger the skill>`
- **Expected trigger:**
  - Skill should load: Yes/No
  - Expected trigger phrase(s): `<keywords>`
- **Prereqs / setup:**
  - `<files, configs, keys, tool access>`
- **Execution notes:**
  - Which SKILL.md section/step should be followed?
  - Which bundled resources should be used?
- **Expected output (observable):**
  - `<file created, text returned, format constraints, invariants>`
- **Pass criteria:**
  - `<objective checks>`
- **If fail, classify:**
  - Triggering / Instructional / Resource / Environment
- **Fix plan:**
  - `<what to change in SKILL.md or resources>`

## Regression Set

When a defect is fixed, add that prompt to a small **regression set** and re-run it after every meaningful change.

## Minimal “Done” Bar for Packaging

Package only when:

- All smoke test cases pass
- `quick_validate.py --comprehensive` has no warnings (or warnings are explicitly accepted)
- Version + CHANGELOG are updated
