# Atomic Commit Principles

Guidelines for identifying logical change boundaries and splitting commits correctly.

---

## What Is an Atomic Commit?

An atomic commit represents **exactly one logical change** to the codebase. It can be:

- Understood in isolation without context from other commits
- Reverted independently without breaking unrelated functionality
- Described with a single coherent sentence

---

## The Core Question

Before deciding whether to group or split changes, ask:

> **"If I revert only this commit, does it break anything unrelated to its stated purpose?"**

- If **yes** → the commit contains unrelated changes → **split it**
- If **no** → the commit is atomic → **it can be kept together**

---

## Split Decision Tree

```
Are there uncommitted changes to analyze?
│
└─► Run: git status, git diff HEAD
    │
    └─► Identify all logical concerns in the changes
        │
        ├─► All changes serve the SAME feature/fix/purpose?
        │   └─► YES → Single commit ✅
        │
        ├─► Changes serve DIFFERENT features or fix DIFFERENT bugs?
        │   └─► YES → Split into separate commits ✅
        │
        ├─► Mix of refactoring + new feature?
        │   └─► YES → Always split ✅
        │
        ├─► Mix of production code + test changes for SAME feature?
        │   └─► YES → Can keep together (tests are part of the feature) ✅
        │
        └─► Unsure?
            └─► ALWAYS split → smaller commits are safer ✅
```

---

## Grouping Rules


| Scenario                                | Decision | Rationale                                         |
| --------------------------------------- | -------- | ------------------------------------------------- |
| New feature + its unit tests            | Group ✅ | Tests are part of the feature delivery            |
| Two different bug fixes                 | Split ✅ | Each fix is independently revertable              |
| New feature + unrelated refactor        | Split ✅ | Refactor obscures the feature diff                |
| UI change + API change for SAME feature | Group ✅ | Same logical change across layers                 |
| CSS formatting + new component logic    | Split ✅ | Style change is independently revertable          |
| Docs update + code change               | Split ✅ | Docs-only changes should be isolated              |
| Multiple files, all part of one fix     | Group ✅ | Logical unity overrides file count                |
| Dependency update + code that uses it   | Group ✅ | Dependency update is incomplete without its usage |

**Default rule:** When in doubt → **always split**.

---

## Common Scenarios

### Scenario 1: Clearly two separate fixes

**Changes found:**

- `src/auth/login.ts` — fixed null pointer when user is not found
- `src/email/mailer.ts` — fixed SMTP timeout configuration

**Decision:** ✅ **Split** — two unrelated bugs in unrelated modules

```
Commit 1: fix(auth): handle null user in login flow
Commit 2: fix(email): increase SMTP timeout to prevent delivery failures
```

---

### Scenario 2: Feature with cross-layer changes

**Changes found:**

- `src/api/users.ts` — new GET /users/:id endpoint
- `src/db/user.repository.ts` — new findById method
- `tests/api/users.test.ts` — tests for the new endpoint

**Decision:** ✅ **Group** — all three files serve the same feature

```
Commit 1: feat(users): add get-user-by-id endpoint with repository and tests
```

---

### Scenario 3: Refactor mixed with new feature

**Changes found:**

- `src/utils/validator.ts` — refactored validation helper structure
- `src/api/register.ts` — new registration endpoint using the refactored helper

**Decision:** ✅ **Split** — refactor should be isolated so it's clearly behavior-neutral

```
Commit 1: refactor(utils): restructure validation helper into class-based pattern
Commit 2: feat(api): add user registration endpoint
```

---

### Scenario 4: Documentation mixed with code

**Changes found:**

- `README.md` — updated setup instructions
- `src/config/env.ts` — added new required environment variable

**Decision:** ✅ **Split** — docs change can be reviewed/reverted independently

```
Commit 1: feat(config): add SMTP_HOST required environment variable
Commit 2: docs(readme): update setup instructions with SMTP_HOST configuration
```

---

### Scenario 5: Multiple small style fixes

**Changes found:**

- `src/auth/login.ts` — removed trailing whitespace
- `src/api/users.ts` — fixed indentation
- `src/email/mailer.ts` — sorted imports

**Decision:** ✅ **Group** — all style-only changes can be one `style` commit

```
Commit 1: style(codebase): remove trailing whitespace and fix import ordering
```

---

## Edge Case: One File Contains Multiple Logical Changes

When a single file has changes belonging to **different logical commits**, use `git add -p` (patch mode) to stage only the relevant hunks:

```bash
git add -p src/auth/service.ts
```

This opens an interactive prompt for each change hunk. Press:

- `y` → stage this hunk
- `n` → skip this hunk
- `s` → split this hunk into smaller parts
- `q` → quit

Commit only the staged hunks, then repeat for the remaining changes.

---

## Commit Ordering

When commits are **dependent on each other**, order them so each commit builds on valid prior state:

1. Infrastructure/config changes first
2. Shared utilities or base classes second
3. Feature implementations that depend on them third
4. Tests last (or bundled with the feature they test)

**Example order:**

```
1. feat(config): add database connection pool configuration
2. feat(db): implement connection pool using new config
3. feat(users): add user repository using connection pool
4. test(users): add integration tests for user repository
```

Never commit a feature before its dependency — the repo must remain in a working state after each commit.
