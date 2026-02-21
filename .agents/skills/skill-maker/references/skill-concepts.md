# Skill Concepts

This document provides foundational knowledge about skills. Load this reference when you need to understand what skills are, how they work, and how to organize them effectively.

## What Are Skills?

Skills are modular, self-contained packages that extend the agent's capabilities:

- Provide specialized knowledge, workflows, and tools
- Transform a general-purpose agent into a specialized agent
- Equip agents with procedural knowledge that no model can fully possess
- Serve as "onboarding guides" for specific domains or tasks
- Intended for AI/LLM consumption, not for humans

### What Skills Provide

- **Specialized workflows** - Multi-step procedures for specific domains
- **Tool integrations** - Instructions for working with specific file formats or APIs
- **Domain expertise** - Company-specific knowledge, schemas, business logic
- **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

## Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
|-- SKILL.md (required)
|   |-- YAML frontmatter metadata (required)
|   |   |-- name: (required)
|   |   |-- description: (required)
|   |   +-- metadata: (required)
|   |       |-- version: (required)  - Semantic versioning (e.g., 1.0.0)
|   |       +-- changelog: (required) - Relative path to CHANGELOG.md
|   +-- Markdown instructions (required)
+-- Bundled Resources (optional)
    |-- CHANGELOG.md      - Version history (required alongside metadata.version)
    |-- scripts/          - Executable code (Python/Bash/etc.)
    |-- references/       - Documentation intended to be loaded into context as needed
    +-- assets/           - Files used in output (templates, icons, fonts, etc.)
```

### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when the agent will use the skill. Use this pattern:

```
This skill guides a complete, [adjective] [domain] workflow from [START], through [MIDDLE], to [END]. This skill must be loaded (NON NEGOTIABLE) whenever user asks to [trigger1], [trigger2], or [catch-all].
```

**Example:**
```
This skill guides a complete, structured skill creation workflow from gathering concrete usage examples and planning reusable contents, through initializing the skill directory and writing effective SKILL.md, to packaging and iterating based on real-world performance. This skill must be loaded (NON NEGOTIABLE) whenever user asks to create or update skills.
```

**Key points:**
- Sentence 1 describes the end-to-end journey (from → through → to) so the agent understands the full scope before loading the skill
- Sentence 2 is the enforcement trigger — use `(NON NEGOTIABLE)` to signal priority
- Be specific and concrete in the journey description — avoid vague terms like "manage" or "handle"
- Keep trigger conditions concise; end with a catch-all (e.g., "or any [domain]-related task")

### Bundled Resources (optional)

#### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by the agent for patching or environment-specific adjustments

#### References (`references/`)

Documentation loaded into context as needed to inform the agent's process.

- **When to include**: For documentation that the agent should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/nda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when the agent determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Place information in either SKILL.md or references files, not both. Keep only essential procedural instructions in SKILL.md; move detailed schemas, examples, and reference material to references files.

#### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output the agent produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables the agent to use files without loading them into context

## Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

- **Metadata (name + description)** - Always in context (~100 words)
- **SKILL.md body** - When skill triggers (<5k words)
- **Bundled resources** - As needed by the agent (unlimited; scripts can execute without loading into context)

## Anti-Patterns

Avoid these common mistakes when creating skills:

### 1. Violating Progressive Disclosure

**Anti-pattern:** Putting everything in SKILL.md.

```
❌ BAD: SKILL.md with 15,000 words of documentation
✅ GOOD: SKILL.md with 2,000 words + references/ for detailed docs
```

**Why it matters:** Large SKILL.md files consume context tokens unnecessarily. The agent may lose important information in the noise.

### 2. Vague Descriptions

**Anti-pattern:** Generic descriptions that don't communicate scope.

```
❌ BAD: "This skill helps with PDF files when needed."
✅ GOOD: "This skill guides a complete PDF manipulation workflow from analyzing document structure, through extracting and modifying content, to saving and validating output. This skill must be loaded (NON NEGOTIABLE) whenever user asks to rotate, merge, split, or extract PDFs."
```

**Why it matters:** Vague descriptions lead to poor skill triggering. The agent won't know when to use the skill.

### 3. Missing Trigger Conditions

**Anti-pattern:** Description without "when" clause.

```
❌ BAD: "This skill guides a workflow for database operations."
✅ GOOD: "This skill guides a complete database migration workflow from schema analysis, through generating migration scripts, to executing and verifying changes. This skill must be loaded (NON NEGOTIABLE) whenever user asks to migrate, upgrade, or modify database schemas."
```

**Why it matters:** Without trigger conditions, the agent has no clear signal for when to load the skill.

### 4. Second-Person Writing

**Anti-pattern:** Using "you" and "your" in instructions.

```
❌ BAD: "You should first check the configuration file, then you can run the script."
✅ GOOD: "Check the configuration file first, then run the script."
```

**Why it matters:** Imperative form is more direct and consumes fewer tokens. It reads like documentation, not conversation.

### 5. Duplicating Content

**Anti-pattern:** Same information in SKILL.md and references/.

```
❌ BAD: SKILL.md contains full API docs AND references/api.md exists with same content
✅ GOOD: SKILL.md links to references/api.md for detailed API documentation
```

**Why it matters:** Duplication wastes tokens and creates maintenance burden. Updates must be made in multiple places.

### 6. Overly Broad Skills

**Anti-pattern:** One skill trying to do everything.

```
❌ BAD: "file-handler" skill for PDF, Excel, Word, images, and JSON
✅ GOOD: Separate skills: "pdf-editor", "excel-processor", "image-manipulator"
```

**Why it matters:** Broad skills are harder to trigger correctly and harder to maintain. Focused skills are more effective.

## When to Create, Update, or Split

Use these rules of thumb to choose the right change.

### Create a new skill

- The same domain workflow is requested repeatedly.
- Trigger phrases are stable and clearly separable from other skills.
- The skill can be described as one coherent journey (from → through → to).

### Update an existing skill

- The skill already triggers correctly, but instructions/resources are incomplete or inefficient.
- New requirements are within the same domain boundary.
- The skill’s structure pattern still fits (workflow/task/guidelines/capabilities).

### Split a skill

Split when triggering or maintenance becomes unreliable.

- **Triggering becomes ambiguous**: >3 distinct trigger groups that rarely overlap.
- **Multiple personas**: different user types need different workflows.
- **Workflow sprawl**: a single workflow exceeds ~8 steps or contains multiple unrelated branches.
- **Mixed domains/tools**: unrelated formats/systems in one skill (e.g., “pdf + excel + images + json”).

Split by **domain boundary** (preferred) or by **operation type** (e.g., “ingestion” vs “reporting”).

### 7. Missing Validation

**Anti-pattern:** No verification that the skill works.

```
❌ BAD: Creating skill and immediately packaging without testing
✅ GOOD: Create → Validate with quick_validate.py --comprehensive → Test with real use cases → Package
```

**Why it matters:** Untested skills may have structural errors or missing required fields.

### 8. Inconsistent Naming

**Anti-pattern:** Mismatch between skill name and directory.

```
❌ BAD: name: "PDFEditor" in a directory called "pdf-tool"
✅ GOOD: name: "pdf-editor" in a directory called "pdf-editor"
```

**Why it matters:** Inconsistency causes confusion and may break tooling that expects matching names.

### 9. No Version Tracking

**Anti-pattern:** Skills without versioning.

```
❌ BAD: No CHANGELOG.md, version stays at 0.0.0
✅ GOOD: Semantic versioning with CHANGELOG.md documenting all changes
```

**Why it matters:** Without versioning, it's impossible to track skill evolution or communicate breaking changes.

### 10. Orphaned Resources

**Anti-pattern:** Files in scripts/, references/, or assets/ that SKILL.md doesn't mention.

```
❌ BAD: scripts/helper.py exists but SKILL.md never references it
✅ GOOD: SKILL.md includes "Use scripts/helper.py for X" in relevant section
```

**Why it matters:** The agent won't know about resources that aren't documented. SKILL.md is the map to the skill's resources.
