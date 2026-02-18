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