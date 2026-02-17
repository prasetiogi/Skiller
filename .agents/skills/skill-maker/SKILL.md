---
name: skill-maker
description: This skill MUST be loaded before creating or updating skills. This skill should be used when the user asks to create or modify skills for extending agent capabilities with specialized knowledge, workflows, or tool integrations.
metadata:
  version: 2.0.0
  changelog: skill-maker/CHANGELOG.md
---

# Skill Maker

This skill standardizes the skill creation process.

## Quick Reference

| Task | Command |
|------|---------|
| Initialize new skill | `scripts/init_skill.py <skill-name> --path <output-directory>` |
| Validate skill | `scripts/quick_validate.py <skill-directory>` |
| Package skill | `scripts/package_skill.py <skill-folder> [output-dir]` |

## References

- **[`references/skill-concepts.md`](references/skill-concepts.md)** - What skills are, anatomy, progressive disclosure principle
- **[`references/structure-patterns.md`](references/structure-patterns.md)** - Workflow, Task, Reference, Capabilities patterns with decision tree

## Skill Creation Process

Follow the process in order, skipping steps only when clearly not applicable.

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

**Example - PDF Editor Skill:**
Query: "Help me rotate this PDF"
Analysis: Rotating a PDF requires re-writing the same code each time
Result: Create `scripts/rotate_pdf.py`

**Example - Frontend Webapp Builder Skill:**
Query: "Build me a todo app" or "Build me a dashboard"
Analysis: Writing a frontend webapp requires the same boilerplate HTML/React each time
Result: Create `assets/hello-world/` template with boilerplate project files

**Example - BigQuery Skill:**
Query: "How many users have logged in today?"
Analysis: Querying BigQuery requires re-discovering table schemas and relationships each time
Result: Create `references/schema.md` documenting table schemas

### Step 3: Initializing the Skill

Skip this step if the skill already exists and only iteration or packaging is needed.

Run the `init_skill.py` script to generate a template skill directory:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates:
- Skill directory with proper structure
- SKILL.md template with frontmatter and TODO placeholders
- CHANGELOG.md for version tracking
- Example resource directories: `scripts/`, `references/`, `assets/`

After initialization, customize or remove the generated files as needed.

### Step 4: Edit the Skill

When editing the skill, remember that it is being created for another agent instance to use. Focus on information that would be beneficial and non-obvious to the agent.

#### Start with Reusable Skill Contents

- Start with the reusable resources identified in Step 2: `scripts/`, `references/`, and `assets/` files
- Request user input if needed (e.g., brand assets for `assets/`, documentation for `references/`)
- Delete example files and directories not needed for the skill

#### Update SKILL.md

**Writing Style:** Write using **imperative form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X").

**Structure Pattern:** Choose a structure that fits the skill's purpose. See [`references/structure-patterns.md`](references/structure-patterns.md) for detailed guidance:

- **Workflow-Based**: Sequential processes
- **Task-Based**: Tool collections
- **Reference/Guidelines**: Standards/specifications
- **Capabilities-Based**: Integrated systems

To complete SKILL.md, answer:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should the agent use the skill? Reference all reusable skill contents.

### Step 5: Packaging a Skill

Once ready, package the skill into a distributable zip file. The packaging script validates automatically:

```bash
scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

The packaging script:
1. **Validates** the skill: frontmatter format, required fields, naming conventions, description quality
2. **Packages** into a zip file named after the skill (e.g., `my-skill.zip`)

If validation fails, fix errors and run again.

### Step 6: Iterate

After testing, users may request improvements based on how the skill performed.

**Iteration workflow:**
- Use the skill on real tasks
- Identify struggles or inefficiencies
- Update SKILL.md or bundled resources as needed
- Implement changes and test again
