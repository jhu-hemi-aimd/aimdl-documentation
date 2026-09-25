---
tags: [tutorials, documentation]
title: "Updating Docs: Info for the Teams"
status: active
owner_team: docs-stewards
last_reviewed: 2026-09-08
review_cycle: 12 months
safety_level: informational
---

# Updating Docs: Info for the Teams

This page is for members of the documentation teams from each subsection including instruments

## 1. Get access (one time)

1. Create a [GitHub account](https://github.com) if you don't have one.
2. Ask a documentation steward to add you to your team on
   `jhu-hemi-aimd/aimdl-documentation` with **write** access, and accept the
   invitation that arrives by email.
3. Clone the repository:

   ```bash
   git clone https://github.com/jhu-hemi-aimd/aimdl-documentation.git
   ```
   you may also use a desktop GitHub app
   

## 2. How a change reaches the site

`main` is protected — nobody edits it directly. Every change follows the same
path: **issue → branch → edits  → commit/push → pull request → review → merge**. This is standard GitHub usage but make sure you understand that you have to make an issue and a relate branch where you work.  Your work doesn't get to the main branch until you make a pull request (PR) and have it reviewed by someone on the Documentation Steward Team. When your PR is approved and merges, the site rebuilds and deploys automatically within a couple of minutes.

Continuous Integration (CI) runs `mkdocs build --strict` on every PR: a broken link, or a page added
without a nav entry (or removed without cleaning up its links), fails the build.

## 3. Step by step

1. **Open an issue** describing the change: which page, what's wrong or
   missing, why. This gives the change a number, say `#12`.
2. **Create a branch** from up-to-date `main`:

   ```bash
   git switch main && git pull
   git switch -c docs/12-maxima-startup
   ```

3. **Write.** Pages are Markdown files under `docs/`, one folder per
   instrument or topic. Start every page with the front matter block below.
   If you *add* a page, add it to `nav:` in `mkdocs.yml`; if you *rename or
   remove* one, update the nav and any links to it in the same commit.
   Preview live while you write:

   ```bash
   pip install -r requirements.txt   # first time only
   mkdocs serve                      # http://127.0.0.1:8000
   ```

4. **Check** before pushing — this is exactly what CI will run:

   ```bash
   mkdocs build --strict
   ```

5. **Commit and push:**

   ```bash
   git add -A
   git commit -m "Add MAXIMA startup procedure (#12)"
   git push -u origin docs/12-maxima-startup
   ```

6. **Open a pull request** on GitHub with `Fixes #12` in the description, and
   request a review from your team's reviewers (safety-critical pages also
   need the lab safety team). When the review is approved and CI is green,
   the PR can be merged — and you're published.

### Front matter template

```yaml
---
title: Page title
status: draft            # draft | active | needs-review | deprecated | archived
owner_team: your-team
primary_contact: TBD
last_reviewed: null
review_cycle: 6 months
safety_level: operational  # informational | operational | safety-critical | restricted
---
```

## 4. The easy way: let a coding agent do the bookkeeping

If you use a coding assistant (GitHub Copilot, Claude Code, etc.) inside your local clone[cite: 1]:

1. Authenticate GitHub CLI: `gh auth login`.
2. Invoke the **`changing-documentation`** skill by prompting your agent:
   > "I would like to change the documentation for [page/topic] with [summary of changes]."
3. The agent will manage the tracking issue, branch setup, front matter boilerplate, `mkdocs build --strict` checks, and draft PR.
4. **You stay responsible for technical accuracy**—always review the diff before requesting merge approval.

Questions? Ask the Documentation Stewards.
