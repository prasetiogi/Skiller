# Conventional Commits Reference

Angular Conventional Commits specification with project-enforced custom rules.

---

## Format Specification

```
type(scope): subject

body paragraph 1 — what changed

body paragraph 2 — why and impact

[optional footer]
```

### Field Rules


| Field     | Required     | Constraint                                            |
| --------- | ------------ | ----------------------------------------------------- |
| `type`    | ✅ MANDATORY | Must be one of the allowed types below                |
| `scope`   | ✅ MANDATORY | Must reflect the affected module/area; NEVER omit     |
| `subject` | ✅ MANDATORY | Imperative mood; max 72 chars; no period at end       |
| `body`    | ✅ MANDATORY | Exactly 2 paragraphs; must cover all 5 aspects        |
| `footer`  | ❌ OPTIONAL  | Include only for breaking changes or issue references |

---

## Type Glossary


| Type       | Use When                                                   |
| ---------- | ---------------------------------------------------------- |
| `feat`     | Introducing new functionality visible to users             |
| `fix`      | Correcting a defect or unintended behavior                 |
| `docs`     | Updating documentation, comments, or README only           |
| `style`    | Formatting changes with no logic impact (whitespace, lint) |
| `refactor` | Code restructuring with no behavior change                 |
| `perf`     | Performance improvement without feature/fix                |
| `test`     | Adding or updating tests only                              |
| `chore`    | Build process, tooling, dependency updates                 |
| `ci`       | Changes to CI/CD configuration or scripts                  |
| `build`    | Changes affecting the build system or compilation          |
| `revert`   | Reverting a previous commit                                |

---

## Scope Guidelines

The scope identifies **which part of the codebase** was affected.

- Use a **noun** that names the module, layer, or feature area (e.g., `auth`, `api`, `ui`, `db`, `validation`, `config`)
- Use **kebab-case** for multi-word scopes (e.g., `user-profile`, `email-queue`)
- Scope should be **specific enough** to locate the change in the codebase
- Avoid generic scopes like `code`, `misc`, `update`, `general`

---

## ⚠️ Custom Rules (Project-Enforced)

These rules are MANDATORY and override default Conventional Commits behavior:

1. **Scope is NEVER optional** — every commit must have a scope in parentheses
2. **Body is NEVER optional** — every commit must have a 2-paragraph body
3. **Body must cover all 5 aspects** — see the Body Writing Guide below
4. **Subject must use imperative mood** — "add feature" not "added feature" or "adds feature"
5. **Subject max 72 characters** — wrap longer descriptions into the body

---

## Body Writing Guide

Write the body in exactly **2 paragraphs** separated by a blank line.

### Paragraph 1 — What Changed

Describe the concrete changes made to the codebase. Cover all that apply:

- What was **added** (new files, functions, endpoints, configs)
- What was **changed** (modified behavior, updated logic, renamed things)
- What was **removed** (deleted code, deprecated features, eliminated dependencies)

Write as a flowing narrative, not a list. If nothing was removed, omit that aspect naturally.

### Paragraph 2 — Why and Impact

Explain the motivation and outcome:

- **Why** this change was necessary (the problem, the gap, the requirement)
- **Impact** on the system, users, or developers (what this enables, fixes, or prevents)

### Self-Check Before Writing

Before finalizing the body, verify:

- [ ]  P1 mentions what was added, changed, and/or removed (whichever apply)
- [ ]  P2 explains the reason this change was needed
- [ ]  P2 explains what the change enables, fixes, or prevents
- [ ]  Both paragraphs read as coherent prose (not bullet lists)
- [ ]  No aspect is vague or generic ("updated some things", "fixed issue")

---

## Footer Specification

Include a footer only when:

- **Breaking change**: Start with `BREAKING CHANGE:` followed by description of what breaks and migration path
- **Issue reference**: `Closes #123`, `Fixes #456`, `Refs #789`
- **Co-author**: `Co-authored-by: Name <email>`

---

## ✅ Good Examples

### Example 1 — Feature with breaking scope

```
feat(auth): add JWT refresh token endpoint

Added a POST /auth/refresh endpoint and updated AuthService to accept both
access and refresh tokens in the validation flow. The token payload schema
was extended to include a refresh_token field alongside the existing access_token.

Users were being logged out after 15 minutes when their access tokens expired,
causing data loss in long-running sessions. This change allows sessions to
persist for up to 7 days via silent token renewal, eliminating unexpected
logouts without requiring users to re-authenticate.
```

### Example 2 — Fix with precise scope

```
fix(validation): correct email regex to accept plus-sign addresses

Updated the email validation regex from /^[\w.-]+@/ to /^[\w.+%-]+@/ to
support RFC 5321 compliant local-part characters. A corresponding test case
was added to cover email addresses containing the '+' character. The
hardcoded rejection of special characters in the local-part was removed.

Users with Gmail-style aliases (user+tag@example.com) were unable to register
or log in, resulting in silent sign-up failures. This fix resolves login
failures for an estimated 12% of users who use email aliasing, as reported
in issue #247.

Closes #247
```

### Example 3 — Refactor preserving behavior

```
refactor(api): extract response serialization into dedicated layer

Moved all JSON response formatting logic from individual route handlers into
a new ResponseSerializer class in src/api/serializers/. Updated all 14 route
handlers to delegate serialization to this class. Removed the duplicate
formatting utilities that had accumulated in utils/response.js.

Response formatting logic had been duplicated across 14 handlers, making it
impossible to enforce consistent error shapes and pagination formats. This
change establishes a single source of truth for API response structure,
enabling consistent formatting changes in one place instead of across all handlers.
```

---

## ❌ Anti-Patterns

### Anti-pattern 1 — Missing scope

```
feat: add login page
```

❌ **Why invalid:** No scope. Cannot identify which part of the codebase this affects.
✅ **Fix:** `feat(ui): add login page`

---

### Anti-pattern 2 — Shallow body (too vague)

```
fix(auth): fix authentication bug

Fixed a bug in the auth module that was causing login failures.

This was needed to fix the bug.
```

❌ **Why invalid:** Body doesn't explain what specifically changed, what the actual bug was, or what impact the fix has.
✅ **Fix:** Describe the exact regex/logic that was wrong, why users were affected, and what the fix enables.

---

### Anti-pattern 3 — Subject in past tense + body missing

```
fix(api): fixed the broken endpoint
```

❌ **Why invalid:** Subject uses past tense ("fixed" → should be "fix"). Body is completely missing.
✅ **Fix:** `fix(api): fix broken endpoint` + add full 2-paragraph body.
