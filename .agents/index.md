# Documentation Agent Skills

Catalog of modular skills available for maintaining and auditing documentation in this repository. Inspect the relevant `SKILL.md` when a user task matches one of the triggers below.

## Available Skills

* **`change-documentation`**
  * **When to use:** Creating new pages, updating existing docs, adding navigation entries, or following the issue-branch-PR contribution workflow.
  * **Path:** `.agents/skills/change-documentation/SKILL.md`

* **`audit-review-cycle`**
  * **When to use:** Auditing page review cycles, identifying unreviewed or expired pages, checking front matter against CODEOWNERS, or generating review tracking issues.
  * **Path:** `.agents/skills/audit-review-cycle/SKILL.md`

---

## Instructions for Agents

1. Match the user's prompt against the **When to use** triggers above.
2. Read the corresponding `SKILL.md` before taking action.
3. Follow the specific workflow, validation scripts, and constraints outlined in that skill's package.
