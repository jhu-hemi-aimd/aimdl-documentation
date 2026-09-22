# Repository Agent Guidelines

You are assisting contributors to the AIMD-L documentation repository.

## Repository Structure

* `docs/`: All documentation content in Markdown. Every file requires complete YAML front matter (`title`, `status`, `owner_team`, `safety_level`, `review_cycle`).
* `mkdocs.yml`: Site navigation tree. Any page added, moved, or deleted must be updated under `nav:`.
* `.agents/skills/`: Executable agent workflows (`SKILL.md`) for tasks like creating pages and auditing review cycles.
* `.github/CODEOWNERS`: Maps directory and file paths to responsible review teams.

## Invariant Rules

1. **Never commit directly to `main`**: All work happens on branches targeting pull requests[cite: 1, 2].
2. **Strict build enforcement**: Always verify changes pass `mkdocs build --strict` before committing[cite: 1, 2]. Broken internal links or orphaned pages break CI[cite: 1, 2].
3. **No inferred procedures**: When drafting instrument guides or safety rules, prompt the user for exact parameters instead of inventing values.
