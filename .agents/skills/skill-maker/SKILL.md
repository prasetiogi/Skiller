---
name: skill-maker
description: This skill MUST be loaded before creating or updating skills. This skill should be used when the user asks to create or modify skills for extending agent capabilities with specialized knowledge, workflows, or tool integrations.
metadata:
  version: 1.2.0
  changelog: skill-maker/CHANGELOG.md
---

# Skill Maker

This skill standardizes the skill creation process.

## About Skills

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

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when the agent will use the skill. Use this pattern:

```
This skill MUST be loaded before [action]. This skill should be used when [trigger conditions] for [purpose].
```

**Example:**
```
This skill MUST be loaded before creating or updating skills. This skill should be used when the user asks to create or modify skills for extending agent capabilities with specialized knowledge, workflows, or tool integrations.
```

**Key points:**
- Use third-person phrasing (`This skill should be used when...` not `Use this skill when...`)
- Be specific about trigger conditions
- Include the skill's purpose

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by the agent for patching or environment-specific adjustments

##### References (`references/`)

Documentation loaded into context as needed to inform the agent's process.

- **When to include**: For documentation that the agent should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/nda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when the agent determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Place information in either SKILL.md or references files, not both. Keep only essential procedural instructions in SKILL.md; move detailed schemas, examples, and reference material to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output the agent produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables the agent to use files without loading them into context

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

- **Metadata (name + description)** - Always in context (~100 words)
- **SKILL.md body** - When skill triggers (<5k words)
- **Bundled resources** - As needed by the agent (unlimited; scripts can execute without loading into context)

## Skill Creation Process

Follow the Skill Creation Process in order, skipping steps only when clearly not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

Understand concrete examples of how the skill will be used. This can come from direct user examples or generated examples validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To prevent overwhelming users, ask questions incrementally rather than all at once.

Conclude this step when the skill's functionality is clearly defined.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

Skip this step if the skill already exists and only iteration or packaging is needed.

When creating a new skill from scratch, run the `init_skill.py` script. This generates a template skill directory with all required files and example resource directories.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another agent instance to use. Focus on including information that would be beneficial and non-obvious to the agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another agent instance execute these tasks more effectively.

#### Start with Reusable Skill Contents

- Start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files
- Request user input if needed (e.g., brand assets for `assets/`, documentation for `references/`)
- Delete example files and directories not needed for the skill

#### Update SKILL.md

**Writing Style:** Write using **imperative form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should the agent use the skill? All reusable skill contents developed above should be referenced so that the agent knows how to use them.

### Step 5: Packaging a Skill

Once the skill is ready, it should be packaged into a distributable zip file that gets shared with the user. The packaging process automatically validates the skill first to ensure it meets all requirements:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory specification:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references

2. **Package** the skill if validation passes, creating a zip file named after the skill (e.g., `my-skill.zip`) that includes all files and maintains the proper directory structure for distribution.

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

### Step 6: Iterate

After testing, users may request improvements based on how the skill performed.

**Iteration workflow:**
- Use the skill on real tasks
- Identify struggles or inefficiencies
- Update SKILL.md or bundled resources as needed
- Implement changes and test again
