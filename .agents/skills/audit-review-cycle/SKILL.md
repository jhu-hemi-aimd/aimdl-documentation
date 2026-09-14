---
name: audit-review-cycle
description: Runs audit.py against docs/ to report overdue review cycles and create GitHub tracking issues.
---

# Review Cycle Audit

## Workflow

1. **Run Audit**
   * Execute the script and relay its output:
     ```bash
     python3 .agents/skills/audit-review-cycle/scripts/audit.py --path docs/
     ```
   
2. **Create Review Issues**
   * Ask the user for confirmation before filing issues for overdue pages.
   * For each confirmed page, run `gh issue create`:
     ```bash
     gh issue create \
       --title "review/<title-of-page>" \
       --body "File: <filename>
     Due: <days_overdue>
     Primary Contact: <primary_contact>
     Reviewers: <@team-slug>"
     ```

## Constraints

* **Read-Only:** Do not edit Markdown files or update front matter dates.
* **No Re-parsing:** Rely entirely on the output of `audit.py` rather than opening or re-reading `.md` files into context.
* **User Confirmation:** Never create issues with `gh issue create` without explicit approval.