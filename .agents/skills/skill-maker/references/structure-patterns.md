# Skill Structure Patterns

This document provides detailed guidance on choosing and implementing the right structure for a skill. Load this reference when designing or restructuring a skill.

## Pattern Overview

Choose a structure that fits the skill's purpose. Patterns can be mixed - most skills combine multiple patterns.


| Pattern                  | Best For                 | Primary Sections                        |
| ------------------------ | ------------------------ | --------------------------------------- |
| **Workflow-Based**       | Sequential processes     | Overview + Workflow + Steps             |
| **Task-Based**           | Tool collections         | Overview + Quick Start + Tasks          |
| **Reference/Guidelines** | Standards/specifications | Overview + Guidelines + Specs           |
| **Capabilities-Based**   | Integrated systems       | Overview + Core Capabilities + Features |

---

## 1. Workflow-Based Pattern

**Use when:** The skill guides users through a defined sequence of steps to accomplish a goal.

**Structure:**

```markdown
# [Skill Name]

## Overview
Brief description of what this workflow accomplishes.

## Workflow
High-level summary of the process.

## Step 1: [First Step]
Details for executing step 1.

## Step 2: [Second Step]
Details for executing step 2.

## Step N: [Final Step]
Details for the final step.

## Troubleshooting
Common issues and solutions.
```

**Example Skills:**

- `skill-maker` - 6-step skill creation process
- `deployment-pipeline` - CI/CD workflow
- `onboarding` - New user setup process

**Best Practices:**

- Number steps clearly
- Include skip conditions at step start
- Add decision points where branching is needed
- End with verification/validation step

---

## 2. Task-Based Pattern

**Use when:** The skill provides a collection of related but independent operations.

**Structure:**

```markdown
# [Skill Name]

## Overview
Brief description of capabilities provided.

## Quick Start
Minimal setup to get started.

## Task 1: [Task Name]
When to use, prerequisites, steps, expected outcome.

## Task 2: [Task Name]
When to use, prerequisites, steps, expected outcome.

## Task N: [Task Name]
When to use, prerequisites, steps, expected outcome.

## Reference
Quick reference for common operations.
```

**Example Skills:**

- `pdf-editor` - Rotate, merge, split, fill forms
- `git-operations` - Branch, merge, rebase, cherry-pick
- `data-transform` - Convert, filter, aggregate, export

**Best Practices:**

- Make tasks independently usable
- Include "When to use" for each task
- Provide a quick reference table
- Order by frequency of use

---

## 3. Reference/Guidelines Pattern

**Use when:** The skill provides standards, conventions, or specifications to follow.

**Structure:**

```markdown
# [Skill Name]

## Overview
What these guidelines cover and why they matter.

## Core Principles
Fundamental rules that guide all decisions.

## Guidelines
Detailed rules organized by category.

## Specifications
Technical details, formats, schemas.

## Examples
Illustrative examples of correct application.

## Anti-Patterns
What to avoid and why.
```

**Example Skills:**

- `code-style` - Language-specific formatting rules
- `api-design` - REST/GraphQL conventions
- `security-guidelines` - Security best practices

**Best Practices:**

- Lead with principles, follow with specifics
- Include both positive and negative examples
- Provide decision trees for complex choices
- Keep specifications in separate reference files

---

## 4. Capabilities-Based Pattern

**Use when:** The skill integrates with a system or API and exposes its functionality.

**Structure:**

```markdown
# [Skill Name]

## Overview
What system this integrates with and what it enables.

## Core Capabilities
High-level categories of functionality.

### Capability 1: [Name]
Description, use cases, related operations.

### Capability 2: [Name]
Description, use cases, related operations.

## Authentication
How to connect and authenticate.

## Common Workflows
Frequent usage patterns.

## API Reference
Detailed operation documentation (or link to references/).
```

**Example Skills:**

- `big-query` - Google BigQuery integration
- `aws-manager` - AWS service operations
- `github-ops` - GitHub API interactions

**Best Practices:**

- Group by capability, not by API endpoint
- Include authentication details upfront
- Provide common workflow examples
- Move detailed API docs to references/

---

## Hybrid Patterns

Most skills combine patterns. Common combinations:


| Combination              | Example                                                        |
| ------------------------ | -------------------------------------------------------------- |
| Workflow + Task          | `skill-maker` - Process steps with task-based scripts          |
| Capabilities + Reference | `api-integration` - Features with detailed specs in references |
| Task + Guidelines        | `code-review` - Tasks with quality standards                   |

**Hybrid Structure Example:**

```markdown
# [Skill Name]

## Overview
...

## Quick Start (Task-Based)
...

## Workflow (Workflow-Based)
...

## Core Capabilities (Capabilities-Based)
...

## Guidelines (Reference/Guidelines)
...

## References
See references/ for detailed specifications.
```

---

## Choosing the Right Pattern

**Decision Tree:**

1. **Is there a defined sequence of steps?**

   - Yes + steps are mandatory: **Workflow-Based**
   - Yes + steps are optional: **Workflow + Task hybrid**
2. **Are operations independent of each other?**

   - Yes: **Task-Based**
3. **Is this primarily about standards and rules?**

   - Yes: **Reference/Guidelines**
4. **Is this about using a system/API?**

   - Yes: **Capabilities-Based**
5. **Multiple answers apply?**

   - Use a **Hybrid** approach
