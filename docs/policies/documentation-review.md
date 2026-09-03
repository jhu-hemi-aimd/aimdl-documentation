---
title: Documentation review
status: active
owner_team: docs-stewards
last_reviewed: 2026-09-03
review_cycle: 12 months
safety_level: informational
---

# Documentation review

## Page metadata

Every maintained page begins with YAML front matter:

```yaml
---
title: MAXIMA startup procedure
status: active            # active | needs-review | draft | deprecated | archived
owner_team: maxima-team
primary_contact: TBD
reviewers:
  - maxima-team
  - lab-safety-team
last_reviewed: 2026-06-01
review_cycle: 6 months
safety_level: operational # informational | operational | safety-critical | restricted
---
```

## Review classes

| Class | Cadence |
| --- | --- |
| Safety-critical | Every 6 months, or after any equipment or procedure change |
| Operational | Every 6–12 months |
| Reference | Annually |
| Tutorial | When software or data dependencies change; at least annually |
| Archived | No routine review; clearly marked |

## When a page becomes `needs-review`

- the instrument changed;
- the software interface changed;
- safety procedures changed;
- a linked data source moved;
- the review date has expired.

## Pull requests

`main` is protected: pull request required, CI (`mkdocs build --strict`) must
pass, code-owner review required for owned paths. Safety-critical pages
additionally require review by the lab safety team.
