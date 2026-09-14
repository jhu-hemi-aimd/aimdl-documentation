---
name: change-documentation
description: Coordinates issue creation, branch setup, content drafting, preflight validation, and pull request submission for aimdl-documentation.
---

# Changing Documentation

## Workflow

1. **Initialize Change**
   * Prompt user for the target page, topic/instrument, and rationale if omitted.
   * Run `gh issue create` and record issue number `N`.
   * Switch and branch: `git switch main && git pull && git switch -c docs/N-<short-slug>`.

2. **Draft Content**
   * If creating a new page, base it on `.agents/templates/new-page.md`.
   * Keep `mkdocs.yml` `nav:` in sync for added, renamed, or deleted files.
   * Prompt the user for missing parameters, steps, or hazards; do not guess operational details.
   * Refer to `.agents/style-guide.md` for documentation standards and conventions.

3. **Validate & Publish**
   * Run the local preflight check and fix reported errors:
     ```bash
     python3 .agents/skills/change-documentation/scripts/preflight.py
     ```
   * Commit referencing `#N` and push branch.
   * Submit PR via `gh pr create` with body `"Fixes #N"`.
   * Inspect page front matter and `.github/CODEOWNERS` to request review from `owner_team` (and add the lab safety team if `safety_level: safety-critical`).
   * Return issue and PR links to the user.

## Constraints

* **Protected Main:** Never commit or push directly to `main`.
* **No Merging:** Do not merge PRs.
* **Preflight Required:** Do not push or open a PR until `preflight.py` passes cleanly.