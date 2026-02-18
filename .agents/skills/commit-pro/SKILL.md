---
name: commit-pro
description: This skill guides a complete, professional git commit workflow from deep analysis of uncommitted changes, through atomic commit splitting, to writing well-documented commit messages and executing them safely. This skill must be loaded (NON NEGOTIABLE) whenever user asks to commit, git commit, or any commit related task.
metadata:
  version: 1.1.0
  changelog: commit-pro/CHANGELOG.md
---

# Professional Commit Workflow

## Overview

This skill guides a complete, professional git commit workflow: from deep analysis of uncommitted changes, through atomic commit splitting, to writing well-documented commit messages and executing them safely. Every commit produced follows Angular Conventional Commits format with mandatory scope and a 2-paragraph narrative body that fully explains what changed, why, and its impact.

## ⚠️ Critical Constraints

These rules are non-negotiable and must be enforced throughout the entire workflow:

- **NEVER use `git add .` or `git add -A`** — always stage specific files or hunks per logical group
- **NEVER use COMMITS.TXT with `git commit -F`** — COMMITS.TXT is a planning document only
- **When in doubt whether to split: ALWAYS split** — smaller atomic commits are always safer
- **Every commit must have a scope** — `type(scope): subject` format is mandatory
- **Every commit must have a 2-paragraph body** — no exceptions

---

## Reference Loading Instructions

Load **both** reference files immediately after reading this skill — before starting any step:

1. Load `references/atomic-commit-principles.md` — required for Step 2 (commit splitting decisions)
2. Load `references/conventional-commits.md` — required for Step 3 (commit message writing)

> **Do not begin the workflow until both references are loaded into context.**

---

## Pre-flight Check

Before starting the workflow, verify:

1. Run `git status` — confirm this is a valid git repository
2. Confirm there are uncommitted changes — if output shows "nothing to commit", stop here
3. Note whether changes are staged, unstaged, or mixed

---

## Step 1: Deep Change Analysis

Gather a complete understanding of every change in the working tree.

### Actions

Run all of the following:

```bash
git status                    # Overview: which files changed, staged vs unstaged
git diff                      # Line-level unstaged changes
git diff --cached             # Line-level staged changes
git diff HEAD                 # All changes combined (staged + unstaged)
git log --oneline -5          # Recent commit context for continuity awareness
```

Additionally, use agentic tools for deeper understanding:

- `read_file` on each changed file — understand its role and full context
- `search_files` — identify cross-file relationships, dependencies, or patterns affected by the changes

### Output

A clear mental model covering every changed file:

- File path → what changed → semantic meaning of the change
- Relationships between changed files

### Gate ✓

> "Can I explain in plain English what every changed file does and why it was modified?"

Do not proceed to Step 2 until the answer is **yes**.

---

## Step 2: Logical Grouping (Atomic Commit Plan)

Identify how many atomic commits the changes should produce. Apply the principles from `references/atomic-commit-principles.md`.

### Actions

1. Apply the split decision tree from `references/atomic-commit-principles.md`
2. Group changed files by logical concern — not by directory or file type
3. Determine the correct order for dependent commits (dependencies commit first)
4. For files containing changes across multiple logical groups: plan to use `git add -p`

### Output

A numbered commit plan in this format:

```
Commit 1: [type(scope): intent] → files: [list]
Commit 2: [type(scope): intent] → files: [list]
...
```

### Gate ✓

> "Is each commit group independently revertable without affecting other groups?"

Do not proceed to Step 3 until the answer is **yes** for every group.

---

## Step 3: Write Commit Messages

Write messages for every planned commit. Follow the format in `references/conventional-commits.md`.

### Phase A — Write Planning Document

Write all commit messages to `.git/COMMITS.TXT` as a planning document for transparency:

```
=== COMMIT PLAN: [N] commits ===

=== COMMIT 1/[N] ===
type(scope): subject

Paragraph 1 — what changed (added, modified, removed)

Paragraph 2 — why this change was needed and what it enables/fixes/prevents

[optional footer]

=== COMMIT 2/[N] ===
...
```

> **Note:** `.git/COMMITS.TXT` is for planning visibility ONLY. Never pass it to `git commit -F`.

### Phase B — Write Execution Files

For each commit, write its message to a dedicated file:

- `.git/COMMIT_MSG_1` → message for commit 1
- `.git/COMMIT_MSG_2` → message for commit 2
- (and so on)

Each file must contain **exactly one** complete commit message (subject + blank line + body + optional footer).

### Body Requirements

Write the body in exactly **2 paragraphs**:

- **Paragraph 1 — What Changed:** Narrative prose covering additions, modifications, and removals (whichever apply). Write as flowing sentences, not a list.
- **Paragraph 2 — Why and Impact:** The motivation (problem/gap/requirement) and the outcome (what this enables, fixes, or prevents).

### Gate ✓ (per commit message)

Before finalizing each message, verify:

- [ ]  Subject uses imperative mood and is under 72 characters
- [ ]  Scope is present in parentheses
- [ ]  P1 covers what was added, changed, and/or removed
- [ ]  P2 explains why and what the impact is
- [ ]  Both paragraphs are specific and informative — no vague language
- [ ]  Type is correct from the allowed type list

Do not proceed to Step 4 until all messages pass this gate.

---

## Step 4: Execute Commits

Execute each commit in the planned order.

### Actions (repeat for each commit group)

```bash
# Stage only the files for this specific commit
git add <file1> <file2> ...

# For files with mixed logical changes, use patch mode instead:
# git add -p <file>

# Commit using the prepared message file
git commit -F .git/COMMIT_MSG_[N]

# Verify the commit landed correctly
git log --oneline -1
```

### Post-Execution Verification

After all commits are done, run:

```bash
git log --oneline -[N]
```

Confirm that:

- All N commits appear in the log
- Each subject line correctly reflects its intent
- Commit order matches the planned dependency order

### Output

Display the final git log summary showing all committed changes.

---

## Quality Gates Summary


| Step   | Gate Question                                | Action if NO                                    |
| ------ | --------------------------------------------- | ---------------------------------------------- |
| Step 1 | Can I explain every change in plain English?  | Continue analyzing with read_file/search_files |
| Step 2 | Is each group independently revertable?       | Re-split the group                             |
| Step 3 | Does each message pass the body checklist?    | Rewrite the body                               |
| Step 4 | Do all N commits appear correctly in the log? | Investigate and amend if needed                |
